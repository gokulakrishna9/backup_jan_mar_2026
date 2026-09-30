"""SQL string builder using PyPika for generating @Query annotation values.

Two-phase approach:
  Phase 1: Build SQL with __P_paramName__ placeholders (avoids PyPika colon issues)
  Phase 2: finalize() replaces __P_paramName__ -> :paramName

All functions return plain SQL strings with no identifier quoting.
"""

from __future__ import annotations
import re
from typing import Optional

from pypika import Query, Table, Criterion, Order
from pypika.terms import ExistsCriterion, ValueWrapper


# ---------------------------------------------------------------------------
# Phase 1: Placeholders
# ---------------------------------------------------------------------------

_PARAM_PREFIX = "__P_"
_PARAM_SUFFIX = "__"
_PARAM_RE = re.compile(r"__P_(\w+)__")


def param(name: str) -> ValueWrapper:
    """Create a placeholder that finalize() will convert to :name."""
    return ValueWrapper(f"{_PARAM_PREFIX}{name}{_PARAM_SUFFIX}")


def literal(value) -> ValueWrapper:
    """Wrap a literal value (1, True, 'text')."""
    return ValueWrapper(value)


# ---------------------------------------------------------------------------
# Phase 2: Finalize
# ---------------------------------------------------------------------------

def finalize(query) -> str:
    """Render query to SQL string and replace placeholders with :params.
    
    Accepts a PyPika QueryBuilder or a raw string.
    """
    sql = query.get_sql(quote_char=None) if hasattr(query, "get_sql") else str(query)
    # Remove any quotes PyPika wraps around our placeholders
    sql = sql.replace(f"'{_PARAM_PREFIX}", _PARAM_PREFIX)
    sql = sql.replace(f"{_PARAM_SUFFIX}'", _PARAM_SUFFIX)
    # Replace __P_name__ -> :name
    sql = _PARAM_RE.sub(r":\1", sql)
    return sql


# ---------------------------------------------------------------------------
# Convenience constructors
# ---------------------------------------------------------------------------

def tables(*names: str) -> tuple[Table, ...]:
    """Create multiple PyPika Table objects."""
    return tuple(Table(n) for n in names)


# ---------------------------------------------------------------------------
# Raw criterion (for patterns PyPika can't express natively)
# ---------------------------------------------------------------------------

class RawCriterion(Criterion):
    """Inject a raw SQL fragment as a WHERE criterion."""

    def __init__(self, sql: str):
        super().__init__()
        self._sql = sql

    def get_sql(self, **kwargs) -> str:
        return self._sql


def raw(sql: str) -> RawCriterion:
    """Shorthand for RawCriterion."""
    return RawCriterion(sql)


# ---------------------------------------------------------------------------
# Clause helpers
# ---------------------------------------------------------------------------

def exists(subquery) -> ExistsCriterion:
    """EXISTS (subquery) criterion."""
    return ExistsCriterion(subquery)


def scalar_eq_true(subquery) -> RawCriterion:
    """(scalar subquery) = true."""
    sql = subquery.get_sql(quote_char=None) if hasattr(subquery, "get_sql") else str(subquery)
    return raw(f"({sql}) = true")


def in_subquery(field_expr: str, subquery) -> RawCriterion:
    """field IN (subquery)."""
    sql = subquery.get_sql(quote_char=None) if hasattr(subquery, "get_sql") else str(subquery)
    return raw(f"{field_expr} IN ({sql})")


def or_(*criteria: Criterion) -> Criterion:
    """Combine criteria with OR."""
    result = criteria[0]
    for c in criteria[1:]:
        result = result | c
    return result


def and_(*criteria: Criterion) -> Criterion:
    """Combine criteria with AND."""
    result = criteria[0]
    for c in criteria[1:]:
        result = result & c
    return result


# ---------------------------------------------------------------------------
# Authorization building blocks
# ---------------------------------------------------------------------------

def super_user_check(auth_param: str = "authUserId") -> RawCriterion:
    """(SELECT is_super_user FROM auth_user WHERE auth_user_id = :p) = true."""
    au = Table("auth_user")
    sub = (Query.from_(au)
           .select(au.is_super_user)
           .where(au.auth_user_id == param(auth_param)))
    return scalar_eq_true(sub)


def super_group_check(auth_param: str = "authUserId") -> ExistsCriterion:
    """EXISTS(user in a super group with active membership)."""
    ugm, ug = tables("user_group_membership", "user_group")
    sub = (
        Query.from_(ugm)
        .join(ug).on(ug.group_id == ugm.group_id)
        .select(literal(1))
        .where(ugm.auth_user_id == param(auth_param))
        .where(raw(
            "(user_group_membership.expires_at IS NULL "
            "OR user_group_membership.expires_at > NOW())"))
        .where(ug.is_super_group == literal(True))
    )
    return exists(sub)


def _active_membership_subquery(auth_param: str = "authUserId") -> str:
    """SQL fragment: subquery returning group_ids for active memberships."""
    ugm = Table("user_group_membership")
    sub = (Query.from_(ugm)
           .select(ugm.group_id)
           .where(ugm.auth_user_id == param(auth_param))
           .where(raw(
               "(user_group_membership.expires_at IS NULL "
               "OR user_group_membership.expires_at > NOW())")))
    return sub.get_sql(quote_char=None)


def table_scope_check(table_name: str,
                      auth_param: str = "authUserId") -> ExistsCriterion:
    """EXISTS(table-level READ via document_group_table_scope)."""
    dgts, dgm = tables("document_group_table_scope", "document_group_membership")
    membership_sub = _active_membership_subquery(auth_param)
    sub = (
        Query.from_(dgts)
        .join(dgm).on(dgm.document_group_id == dgts.document_group_id)
        .select(literal(1))
        .where(dgts.table_name == literal(table_name))
        .where(dgts.allow_read == literal(True))
        .where(raw(
            "(document_group_membership.expires_at IS NULL "
            "OR document_group_membership.expires_at > NOW())"))
        .where(or_(
            dgm.auth_user_id == param(auth_param),
            in_subquery("document_group_membership.user_group_id", raw(membership_sub))
        ))
    )
    return exists(sub)


def record_scope_check(table_name: str, id_column: str,
                       table_alias: str = "t",
                       auth_param: str = "authUserId") -> ExistsCriterion:
    """EXISTS(record-level READ via document_group_table_record_scope)."""
    dgtrs, dgm = tables("document_group_table_record_scope", "document_group_membership")
    membership_sub = _active_membership_subquery(auth_param)
    sub = (
        Query.from_(dgtrs)
        .join(dgm).on(dgm.document_group_id == dgtrs.document_group_id)
        .select(literal(1))
        .where(dgtrs.table_name == literal(table_name))
        .where(raw(f"document_group_table_record_scope.record_id = {table_alias}.{id_column}"))
        .where(dgtrs.allow_read == literal(True))
        .where(raw(
            "(document_group_membership.expires_at IS NULL "
            "OR document_group_membership.expires_at > NOW())"))
        .where(or_(
            dgm.auth_user_id == param(auth_param),
            in_subquery("document_group_membership.user_group_id", raw(membership_sub))
        ))
    )
    return exists(sub)


def auth_where(table_name: str, id_column: str,
               table_alias: str = "t",
               auth_param: str = "authUserId") -> Criterion:
    """Full authorization OR criterion: super_user OR super_group OR table_scope OR record_scope."""
    return or_(
        super_user_check(auth_param),
        super_group_check(auth_param),
        table_scope_check(table_name, auth_param),
        record_scope_check(table_name, id_column, table_alias, auth_param),
    )


# ---------------------------------------------------------------------------
# High-level query builders
# ---------------------------------------------------------------------------

def auth_paged_query(table_name: str, id_column: str,
                     soft_delete: bool = True) -> str:
    """Build authorized paginated SELECT for a table. Returns finalized SQL."""
    t = Table(table_name).as_("t")
    q = Query.from_(t).select(raw(f"DISTINCT t.*"))
    if soft_delete:
        q = q.where(t.field("deleted_at").isnull())
    q = q.where(auth_where(table_name, id_column))
    q = q.orderby(t.field(id_column))
    # PyPika limit/offset with placeholders
    sql = q.get_sql(quote_char=None)
    sql += f" LIMIT {_PARAM_PREFIX}size{_PARAM_SUFFIX} OFFSET {_PARAM_PREFIX}offset{_PARAM_SUFFIX}"
    return finalize(raw(sql))


def auth_count_query(table_name: str, id_column: str,
                     soft_delete: bool = True) -> str:
    """Build authorized COUNT for a table. Returns finalized SQL."""
    t = Table(table_name).as_("t")
    q = Query.from_(t).select(raw(f"COUNT(DISTINCT t.{id_column})"))
    if soft_delete:
        q = q.where(t.field("deleted_at").isnull())
    q = q.where(auth_where(table_name, id_column))
    return finalize(q)


def paged_query(table_name: str, id_column: str,
                soft_delete: bool = True) -> str:
    """Build simple (no auth) paginated SELECT. Returns finalized SQL."""
    t = Table(table_name)
    q = Query.from_(t).select(t.star)
    if soft_delete:
        q = q.where(t.field("deleted_at").isnull())
    q = q.orderby(t.field(id_column))
    sql = q.get_sql(quote_char=None)
    sql += f" LIMIT {_PARAM_PREFIX}size{_PARAM_SUFFIX} OFFSET {_PARAM_PREFIX}offset{_PARAM_SUFFIX}"
    return finalize(raw(sql))


def simple_count_query(table_name: str,
                       soft_delete: bool = True) -> str:
    """Build simple (no auth) COUNT. Returns finalized SQL."""
    t = Table(table_name)
    q = Query.from_(t).select(raw("COUNT(*)"))
    if soft_delete:
        q = q.where(t.field("deleted_at").isnull())
    return finalize(q)

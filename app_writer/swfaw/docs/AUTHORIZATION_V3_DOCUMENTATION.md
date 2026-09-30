# Authorization Layer v3.0 - Complete Documentation

**Version:** 3.0.0  
**Date:** March 11, 2026  
**Status:** ✅ Design Complete - Implementation In Progress

---

## Table of Contents

1. [Overview](#overview)
2. [Key Changes from v2.x](#key-changes-from-v2x)
3. [Architecture](#architecture)
4. [Database Schema](#database-schema)
5. [Document Group Types](#document-group-types)
6. [Access Control Model](#access-control-model)
7. [Authorization Flow](#authorization-flow)
8. [Usage Examples](#usage-examples)
9. [Java Implementation](#java-implementation)
10. [Application Definition](#application-definition)
11. [Migration Guide](#migration-guide)

---

## Overview

Authorization Layer v3.0 introduces a revolutionary approach to document-based access control with:

- **Creator-based default access:** Users automatically have full access to records they create
- **Per-table access controls:** Each table in a document group can have different permissions
- **Per-record access controls:** Individual records can have granular permissions
- **Query-based read-only views:** Queries provide READ-only access to filtered data
- **Simplified permission model:** Access controls embedded in scope tables (no separate permission table)
- **Table-level roles:** USER (read-only) and ADMIN (full CRUD) access levels

### Core Principles

1. **Default Security:** Users can only access their own data by default
2. **Explicit Grants:** Additional access must be explicitly granted
3. **Granular Control:** Permissions at table, record, and query levels
4. **Performance:** Direct boolean checks instead of complex joins
5. **Clarity:** Self-documenting schema with clear relationships

---

## Key Changes from v2.x

### Removed Tables

- ❌ `access_control` - Replaced by boolean flags in scope tables
- ❌ `document_group_definition` - Replaced by 4 specialized scope tables
- ❌ `document_permission` - Replaced by `document_group_membership`

### Added Tables

- ✅ `document_group_table_scope` - Entire table access with ACL flags
- ✅ `document_group_table_record_scope` - Specific record access with ACL flags
- ✅ `document_group_query_scope` - Query-based READ-only views
- ✅ `document_group_query_record_scope` - Specific records for queries
- ✅ `document_group_membership` - Simplified user/group membership

### Schema Evolution

```
v2.x: 13 tables
v3.0: 15 tables (+2 tables for better separation of concerns)

Old Model:
  document_group → document_group_definition → document_permission → access_control
  
New Model:
  document_group → [table_scope | record_scope | query_scope] → document_group_membership
                   (ACLs embedded)      (ACLs embedded)    (READ-only)
```

### Key Improvements

1. **Per-table ACLs:** Different permissions for each table in a document group
2. **Per-record ACLs:** Different permissions for each record
3. **Creator tracking:** All business tables track `created_by_auth_user_id`
4. **Query views:** Queries are READ-only views (no write operations)
5. **Simpler model:** No separate access_control table needed
6. **Better performance:** Direct boolean checks, indexed lookups

---

## Architecture

### Conceptual Model

```
┌─────────────────────────────────────────────────────────────┐
│                    Authorization Hierarchy                   │
├─────────────────────────────────────────────────────────────┤
│ 1. Super User / Super Group → Full access to everything     │
│ 2. Creator → Full access to own records (default)           │
│ 3. Table Admin → Full access to all records in table        │
│ 4. Table User → Read-only access to all records in table    │
│ 5. Specific Records → Access to explicitly granted records  │
│ 6. Query-Based → READ-only access based on query conditions │
│ 7. Deny → No access                                         │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

```
User Request (table_name, record_id, operation)
    ↓
┌───────────────────────────────────────┐
│ 1. Check Super User/Super Group       │
│    → Grant all access                 │
└───────────────────────────────────────┘
    ↓ (if not super)
┌───────────────────────────────────────┐
│ 2. Check Creator                      │
│    → Query: created_by_auth_user_id   │
│    → Grant all access to own records  │
└───────────────────────────────────────┘
    ↓ (if not creator)
┌───────────────────────────────────────┐
│ 3. Find Document Groups               │
│    → document_group_membership        │
│    → Get user's document groups       │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ 4. Check Table Scope                  │
│    → document_group_table_scope       │
│    → Check ACL flags (allow_read, etc)│
└───────────────────────────────────────┘
    ↓ (if no table access)
┌───────────────────────────────────────┐
│ 5. Check Record Scope                 │
│    → document_group_table_record_scope│
│    → Check ACL flags for this record  │
└───────────────────────────────────────┘
    ↓ (if no record access)
┌───────────────────────────────────────┐
│ 6. Check Query Scope (READ only)      │
│    → document_group_query_scope       │
│    → Execute query from registry      │
│    → Grant READ if query matches      │
└───────────────────────────────────────┘
    ↓
┌───────────────────────────────────────┐
│ 7. Log Access Attempt                 │
│    → access_audit_log                 │
│    → Record granted/denied            │
└───────────────────────────────────────┘
    ↓
Return: true (granted) or false (denied)
```

---

## Database Schema

### Complete Schema (15 Tables)

#### System Configuration (1 table)

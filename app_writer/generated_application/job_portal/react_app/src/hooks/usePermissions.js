import { useMemo } from 'react';

/**
 * Decode a JWT token payload (base64url).
 */
function decodeJwt(token) {
  try {
    const payload = token.split('.')[1];
    const padded = payload + '='.repeat((4 - payload.length % 4) % 4);
    return JSON.parse(atob(padded));
  } catch {
    return null;
  }
}

/**
 * Hook that derives permissions from JWT claims (roles, tableAccess).
 * SUPER_ADMIN: full access to everything.
 * TABLE_ADMIN: access based on tableAccess claim for the matching table.
 * USER: all operations allowed (backend service layer handles record-level filtering).
 * @param {string} basePath - The API base path (e.g. '/api/user_profiles')
 */
const usePermissions = (basePath) => {
  const token = localStorage.getItem('token');

  const permissions = useMemo(() => {
    if (!token) {
      return { canCreate: false, canView: false, canUpdate: false, canDelete: false, canList: false, canGrantAccess: false };
    }

    const claims = decodeJwt(token);
    if (!claims) {
      return { canCreate: false, canView: false, canUpdate: false, canDelete: false, canList: false, canGrantAccess: false };
    }

    // roles may be an array of objects, array of strings, or a JSON string
    let rawRoles = claims.roles || [];
    if (typeof rawRoles === 'string') {
      try { rawRoles = JSON.parse(rawRoles); } catch { rawRoles = []; }
    }
    if (!Array.isArray(rawRoles)) rawRoles = [];
    const roles = rawRoles.map(r => typeof r === 'string' ? r : (r && r.role ? r.role : ''));

    // SUPER_ADMIN: full access
    if (roles.includes('SUPER_ADMIN')) {
      return { canCreate: true, canView: true, canUpdate: true, canDelete: true, canList: true, canGrantAccess: true };
    }

    // Derive table name from basePath: /api/user_profiles -> user_profiles, then strip trailing 's' for table match
    const pathSegment = basePath.replace(/^\/api\//, '');
    let tableAccess = claims.tableAccess || {};
    if (typeof tableAccess === 'string') {
      try { tableAccess = JSON.parse(tableAccess); } catch { tableAccess = {}; }
    }

    // Check tableAccess for this path segment (TABLE_ADMIN)
    const ops = tableAccess[pathSegment] || [];
    if (ops.length > 0) {
      return {
        canCreate: ops.includes('CREATE'),
        canView: ops.includes('READ'),
        canUpdate: ops.includes('UPDATE'),
        canDelete: ops.includes('DELETE'),
        canList: ops.includes('READ'),
        canGrantAccess: false,
      };
    }

    // USER role: allow all operations (backend handles record-level filtering)
    if (roles.includes('USER') || roles.length > 0) {
      return { canCreate: true, canView: true, canUpdate: true, canDelete: true, canList: true, canGrantAccess: false };
    }

    return { canCreate: false, canView: false, canUpdate: false, canDelete: false, canList: false, canGrantAccess: false };
  }, [token, basePath]);

  return permissions;
};

export { usePermissions };
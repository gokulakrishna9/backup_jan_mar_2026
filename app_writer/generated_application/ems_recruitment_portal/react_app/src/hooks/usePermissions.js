import { useCallback } from 'react';
import { useAuth } from '../auth/AuthContext';

/**
 * Hook that checks user permissions against the allowedApiList from AuthContext.
 * Each entry in allowedApiList is { method: 'GET', path: '/api/entity' } or { method: 'GET', path: '/api/entity/*' }.
 * Supports wildcard matching: /api/entity/* matches /api/entity/{id} and similar suffixed paths.
 * @param {string} basePath - The API base path (e.g. '/api/jobApplications')
 */
const usePermissions = (basePath) => {
  const { allowedApiList } = useAuth();

  const hasPermission = useCallback(
    (method, pathSuffix = '') => {
      const targetPath = basePath + pathSuffix;
      return allowedApiList.some((entry) => {
        if (entry.method !== method) return false;
        if (entry.path === targetPath) return true;
        // Wildcard: /api/entity/* matches /api/entity/{id}, /api/entity/anything
        if (entry.path.endsWith('/*')) {
          const wildcardBase = entry.path.slice(0, -2);
          return targetPath.startsWith(wildcardBase + '/');
        }
        return false;
      });
    },
    [allowedApiList, basePath]
  );

  const canCreate = hasPermission('POST');
  const canView = hasPermission('GET', '/{id}');
  const canUpdate = hasPermission('PUT', '/{id}');
  const canDelete = hasPermission('DELETE', '/{id}');
  const canList = hasPermission('GET');
  const canGrantAccess = hasPermission('POST', '/grant-access');

  return { canCreate, canView, canUpdate, canDelete, canList, canGrantAccess };
};

export { usePermissions };
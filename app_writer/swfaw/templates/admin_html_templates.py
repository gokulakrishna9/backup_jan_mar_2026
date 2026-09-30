"""Thymeleaf HTML templates for admin UI."""


class AdminHTMLTemplates:
    """HTML templates for admin interface."""
    
    # Dashboard
    DASHBOARD_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .header h1 { font-size: 1.5rem; }
        .header .user-info { float: right; margin-top: -2rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { margin-bottom: 1rem; color: #2c3e50; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
        .menu-item { background: #3498db; color: white; padding: 2rem; border-radius: 8px; text-align: center; text-decoration: none; display: block; transition: background 0.3s; }
        .menu-item:hover { background: #2980b9; }
        .menu-item h3 { margin-bottom: 0.5rem; }
        .menu-item p { opacity: 0.9; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Admin Dashboard</h1>
        <div class="user-info">
            <span th:text="${currentUser.username}">Admin</span> | 
            <a href="/logout" style="color: white;">Logout</a>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2>Administration</h2>
            <div class="grid">
                <a href="/admin/groups" class="menu-item">
                    <h3>User Groups</h3>
                    <p>Manage user groups and default groups</p>
                </a>
                <a href="/admin/users" class="menu-item">
                    <h3>Users</h3>
                    <p>Manage users and their group memberships</p>
                </a>
                <a href="/admin/document-groups" class="menu-item">
                    <h3>Document Groups</h3>
                    <p>Manage document groups and permissions</p>
                </a>
                <a href="/api/audit/denied-access" class="menu-item">
                    <h3>Audit Logs</h3>
                    <p>View access logs and security events</p>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
"""

    # Groups List
    GROUPS_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Groups</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; }
        .btn:hover { background: #2980b9; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; }
        .badge-success { background: #27ae60; color: white; }
        .badge-warning { background: #f39c12; color: white; }
        .alert { padding: 1rem; margin-bottom: 1rem; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>User Groups</h1>
        <a href="/admin">← Back to Dashboard</a>
    </div>
    
    <div class="container">
        <div class="card">
            <p style="color: #666; margin-bottom: 1rem;">
                <span class="badge badge-info" style="background: #3498db;">System-Managed</span>
                Groups are prepopulated during application setup. Use this page to view groups and manage user membership.
            </p>
            
            <table>
                <thead>
                    <tr>
                        <th>Group Name</th>
                        <th>Description</th>
                        <th>Type</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="group : ${groups}">
                        <td th:text="${group.groupName}">Group Name</td>
                        <td th:text="${group.description}">Description</td>
                        <td>
                            <span th:if="${group.isSuperGroup}" class="badge badge-warning">Super Group</span>
                            <span th:if="${group.isDefaultGroup}" class="badge badge-success">Default</span>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    # Group Form (replaced with read-only notice - groups are system-managed)
    GROUP_FORM_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Groups - System Managed</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 600px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn-secondary { display: inline-block; padding: 0.5rem 1.5rem; background: #95a5a6; color: white; text-decoration: none; border-radius: 4px; }
        .btn-secondary:hover { background: #7f8c8d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Groups - System Managed</h1>
        <a href="/admin/groups">&larr; Back to Groups</a>
    </div>
    <div class="container">
        <div class="card">
            <p>User groups are prepopulated during application setup from the group definition layer.</p>
            <p style="margin-top:1rem;">To modify groups, update <code>group_definition_layer.json</code> and regenerate the application.</p>
            <p style="margin-top:1rem;"><a href="/admin/groups" class="btn-secondary">Back to Groups</a></p>
        </div>
    </div>
</body>
</html>
"""

    # Users List
    USERS_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Users</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .btn:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; background: #3498db; color: white; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Users</h1>
        <a href="/admin">← Back to Dashboard</a>
    </div>
    
    <div class="container">
        <div class="card">
            <table>
                <thead>
                    <tr>
                        <th>Username</th>
                        <th>Email</th>
                        <th>Super User</th>
                        <th>Created</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="user : ${users}">
                        <td th:text="${user.username}">username</td>
                        <td th:text="${user.email}">email@example.com</td>
                        <td>
                            <span th:if="${user.isActive}" class="badge">Active</span>
                        </td>
                        <td th:text="${#temporals.format(user.createdAt, 'yyyy-MM-dd')}">2024-01-01</td>
                        <td>
                            <a th:href="@{/admin/users/{id}(id=${user.authUserId})}" class="btn">Manage</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""


    # User Detail
    USER_DETAIL_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Details</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { margin-bottom: 1rem; color: #2c3e50; }
        .info-grid { display: grid; grid-template-columns: 150px 1fr; gap: 0.5rem; margin-bottom: 1rem; }
        .info-label { font-weight: 600; }
        .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; }
        .btn:hover { background: #2980b9; }
        .btn-danger { background: #e74c3c; }
        .btn-danger:hover { background: #c0392b; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .badge { display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; background: #3498db; color: white; }
        .form-inline { display: flex; gap: 0.5rem; align-items: center; margin-top: 1rem; }
        select { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
        .alert { padding: 1rem; margin-bottom: 1rem; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>User Details</h1>
        <a href="/admin/users">← Back to Users</a>
    </div>
    
    <div class="container">
        <div th:if="${param.success}" class="alert alert-success">
            <span th:if="${param.success[0] == 'group_added'}">User added to group successfully!</span>
            <span th:if="${param.success[0] == 'group_removed'}">User removed from group successfully!</span>
        </div>
        
        <div class="card">
            <h2>User Information</h2>
            <div class="info-grid">
                <div class="info-label">Username:</div>
                <div th:text="${user.username}">username</div>
                
                <div class="info-label">Email:</div>
                <div th:text="${user.email}">email@example.com</div>
                
                <div class="info-label">Active:</div>
                <div>
                    <span th:if="${user.isActive}" class="badge">Yes</span>
                    <span th:unless="${user.isActive}">No</span>
                </div>
                
                <div class="info-label">Created:</div>
                <div th:text="${#temporals.format(user.createdAt, 'yyyy-MM-dd HH:mm')}">2024-01-01 12:00</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Group Memberships</h2>
            <table>
                <thead>
                    <tr>
                        <th>Group Name</th>
                        <th>Type</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="group : ${userGroups}">
                        <td th:text="${group.groupName}">Group Name</td>
                        <td>
                            <span th:if="${group.isSuperGroup}" class="badge">Super Group</span>
                        </td>
                        <td>
                            <form th:action="@{/admin/users/{userId}/groups/{groupId}/remove(userId=${user.authUserId},groupId=${group.groupId})}" method="post" style="display: inline;">
                                <button type="submit" class="btn btn-danger" onclick="return confirm('Remove from group?')">Remove</button>
                            </form>
                        </td>
                    </tr>
                    <tr th:if="${#lists.isEmpty(userGroups)}">
                        <td colspan="3" style="text-align: center; color: #999;">No group memberships</td>
                    </tr>
                </tbody>
            </table>
            
            <form class="form-inline" th:action="@{/admin/users/{userId}/groups/{groupId}/add(userId=${user.authUserId},groupId=0)}" method="post">
                <select name="groupId" required>
                    <option value="">Select a group...</option>
                    <option th:each="group : ${allGroups}" th:value="${group.groupId}" th:text="${group.groupName}">Group</option>
                </select>
                <button type="submit" class="btn">Add to Group</button>
            </form>
        </div>
        
        <div class="card">
            <h2>Direct Permissions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Document Group</th>
                        <th>Access Control</th>
                        <th>Valid Until</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="permission : ${permissions}">
                        <td th:text="${permission.documentGroupId}">Doc Group ID</td>
                        <td th:text="${permission.accessControlId}">Access Control</td>
                        <td th:text="${permission.validUntil != null ? #temporals.format(permission.validUntil, 'yyyy-MM-dd') : 'Permanent'}">Permanent</td>
                    </tr>
                    <tr th:if="${#lists.isEmpty(permissions)}">
                        <td colspan="3" style="text-align: center; color: #999;">No direct permissions</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    # Document Groups List
    DOCUMENT_GROUPS_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Groups</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; }
        .btn:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .alert { padding: 1rem; margin-bottom: 1rem; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Document Groups</h1>
        <a href="/admin">← Back to Dashboard</a>
    </div>
    
    <div class="container">
        <div class="card">
            <p style="color: #666; margin-bottom: 1rem;">
                <span style="display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; background: #3498db; color: white;">System-Managed</span>
                Document groups are prepopulated during application setup. Use this page to view groups and manage permissions.
            </p>
            
            <table>
                <thead>
                    <tr>
                        <th>Group Name</th>
                        <th>Description</th>
                        <th>Type</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="docGroup : ${documentGroups}">
                        <td th:text="${docGroup.groupName}">Group Name</td>
                        <td th:text="${docGroup.description}">Description</td>
                        <td th:text="${docGroup.groupTypeId}">Type ID</td>
                        <td>
                            <a th:href="@{/admin/document-groups/{id}(id=${docGroup.documentGroupId})}" class="btn">Manage</a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

    # Document Group Form (replaced with read-only notice - groups are system-managed)
    DOCUMENT_GROUP_FORM_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Groups - System Managed</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 600px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .btn-secondary { display: inline-block; padding: 0.5rem 1.5rem; background: #95a5a6; color: white; text-decoration: none; border-radius: 4px; }
        .btn-secondary:hover { background: #7f8c8d; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Document Groups - System Managed</h1>
        <a href="/admin/document-groups">&larr; Back to Document Groups</a>
    </div>
    <div class="container">
        <div class="card">
            <p>Document groups are prepopulated during application setup from the group definition layer.</p>
            <p style="margin-top:1rem;">To modify document groups, update <code>group_definition_layer.json</code> and regenerate the application.</p>
            <p style="margin-top:1rem;"><a href="/admin/document-groups" class="btn-secondary">Back to Document Groups</a></p>
        </div>
    </div>
</body>
</html>
"""

    # Document Group Detail (with definitions and permissions)
    DOCUMENT_GROUP_DETAIL_HTML = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Group Details</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 1rem 2rem; }
        .header h1 { font-size: 1.5rem; display: inline-block; }
        .header a { color: white; text-decoration: none; float: right; margin-top: 0.3rem; }
        .container { max-width: 1200px; margin: 2rem auto; padding: 0 2rem; }
        .card { background: white; border-radius: 8px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .card h2 { margin-bottom: 1rem; color: #2c3e50; }
        .info-grid { display: grid; grid-template-columns: 150px 1fr; gap: 0.5rem; margin-bottom: 1rem; }
        .info-label { font-weight: 600; }
        .btn { display: inline-block; padding: 0.5rem 1rem; background: #3498db; color: white; text-decoration: none; border-radius: 4px; border: none; cursor: pointer; }
        .btn:hover { background: #2980b9; }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #f8f9fa; font-weight: 600; }
        .form-inline { display: flex; gap: 0.5rem; align-items: flex-end; margin-top: 1rem; flex-wrap: wrap; }
        .form-group-inline { display: flex; flex-direction: column; }
        .form-group-inline label { font-size: 0.85rem; margin-bottom: 0.25rem; }
        input[type="text"], select, textarea { padding: 0.5rem; border: 1px solid #ddd; border-radius: 4px; }
        textarea { min-width: 300px; min-height: 60px; }
        .alert { padding: 1rem; margin-bottom: 1rem; border-radius: 4px; }
        .alert-success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        code { background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; font-size: 0.9rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Document Group Details</h1>
        <a href="/admin/document-groups">← Back to Document Groups</a>
    </div>
    
    <div class="container">
        <div th:if="${param.success}" class="alert alert-success">
            <span th:if="${param.success[0] == 'permission_granted'}">Permission granted successfully!</span>
        </div>
        
        <div class="card">
            <h2>Group Information</h2>
            <p style="color: #666; margin-bottom: 1rem;">
                <span style="display: inline-block; padding: 0.25rem 0.5rem; border-radius: 4px; font-size: 0.85rem; background: #3498db; color: white;">System-Managed</span>
                This group was prepopulated during application setup.
            </p>
            <div class="info-grid">
                <div class="info-label">Group Name:</div>
                <div th:text="${documentGroup.groupName}">Group Name</div>
                
                <div class="info-label">Description:</div>
                <div th:text="${documentGroup.description}">Description</div>
                
                <div class="info-label">Type ID:</div>
                <div th:text="${documentGroup.groupTypeId}">Type</div>
            </div>
        </div>
        
        <div class="card">
            <h2>Document Definitions</h2>
            <table>
                <thead>
                    <tr>
                        <th>Table Name</th>
                        <th>Record IDs</th>
                        <th>Query Definition</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="def : ${definitions}">
                        <td th:text="${def.tableName}">table_name</td>
                        <td><code th:text="${def.recordIds}">1,2,3</code></td>
                        <td><code th:text="${def.queryDefinition}">query</code></td>
                    </tr>
                    <tr th:if="${#lists.isEmpty(definitions)}">
                        <td colspan="3" style="text-align: center; color: #999;">No definitions</td>
                    </tr>
                </tbody>
            </table>
            
            <p style="color: #999; margin-top: 1rem; font-size: 0.9rem;">
                Document definitions are prepopulated during application setup. To modify, update <code>group_definition_layer.json</code> and regenerate.
            </p>
        </div>
        
        <div class="card">
            <h2>Permissions</h2>
            <table>
                <thead>
                    <tr>
                        <th>User/Group</th>
                        <th>Access Control</th>
                        <th>Valid Until</th>
                    </tr>
                </thead>
                <tbody>
                    <tr th:each="perm : ${permissions}">
                        <td>
                            <span th:if="${perm.authUserId != null}">User ID: <span th:text="${perm.authUserId}">1</span></span>
                            <span th:if="${perm.userGroupId != null}">Group ID: <span th:text="${perm.userGroupId}">1</span></span>
                        </td>
                        <td th:text="${perm.accessControlId}">Control</td>
                        <td th:text="${perm.validUntil != null ? #temporals.format(perm.validUntil, 'yyyy-MM-dd') : 'Permanent'}">Permanent</td>
                    </tr>
                    <tr th:if="${#lists.isEmpty(permissions)}">
                        <td colspan="3" style="text-align: center; color: #999;">No permissions</td>
                    </tr>
                </tbody>
            </table>
            
            <form class="form-inline" th:action="@{/admin/document-groups/{id}/permissions(id=${documentGroup.documentGroupId})}" method="post">
                <div class="form-group-inline">
                    <label>User Group</label>
                    <select name="userGroupId">
                        <option value="">Select group...</option>
                        <option th:each="group : ${userGroups}" th:value="${group.groupId}" th:text="${group.groupName}">Group</option>
                    </select>
                </div>
                <div class="form-group-inline">
                    <label>Access Control *</label>
                    <select name="accessControlId" required>
                        <option value="">Select control...</option>
                        <option th:each="control : ${accessControls}" th:value="${control.controlId}" th:text="${control.controlName}">Control</option>
                    </select>
                </div>
                <button type="submit" class="btn">Grant Permission</button>
            </form>
        </div>
    </div>
</body>
</html>
"""

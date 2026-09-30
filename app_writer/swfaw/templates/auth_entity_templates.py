"""Authentication entity templates for code generation."""


class AuthEntityTemplates:
    """Templates for authentication/authorization entity generation."""
    
    # System Config Entity
    SYSTEM_CONFIG_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("system_config")
public class SystemConfig {
    
    @Id
    private String configKey;
    private String configValue;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
}
"""

    # Auth User Entity
    AUTH_USER_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("auth_user")
public class AuthUser {
    
    @Id
    private Long authUserId;
    private String username;
    private String email;
    private String passwordHash;
    private Boolean isActive;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    @org.springframework.data.annotation.Transient
    private java.util.List<String> roles;
}
"""

    # Access Audit Log Entity
    ACCESS_AUDIT_LOG_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("access_audit_log")
public class AccessAuditLog {
    
    @Id
    private Long auditId;
    private Long authUserId;
    private String action;
    private String tableName;
    private Long recordId;
    private Boolean accessGranted;
    private String denialReason;
    private String ipAddress;
    private String userAgent;
    private LocalDateTime accessedAt;
}
"""

    # User Role Entity
    USER_ROLE_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("user_role")
public class UserRole {
    
    @Id
    private Long userRoleId;
    private Long authUserId;
    private String role;
    private String tableName;
    private LocalDateTime grantedAt;
    private Long grantedByAuthUserId;
}
"""

    # Record Owner Entity
    RECORD_OWNER_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("record_owner")
public class RecordOwner {
    
    @Id
    private Long recordOwnerId;
    private Long authUserId;
    private String tableName;
    private Long recordId;
    private LocalDateTime createdAt;
}
"""

    # Query Group Entity
    QUERY_GROUP_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("query_group")
public class QueryGroup {
    
    @Id
    private Long queryGroupId;
    private String groupName;
    private String groupType;
    private Long ownerAuthUserId;
    private String description;
    private LocalDateTime createdAt;
}
"""

    # Query Group Query Entity
    QUERY_GROUP_QUERY_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("query_group_query")
public class QueryGroupQuery {
    
    @Id
    private Long queryGroupQueryId;
    private Long queryGroupId;
    private String queryName;
}
"""

    # Query Group Member Entity
    QUERY_GROUP_MEMBER_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("query_group_member")
public class QueryGroupMember {
    
    @Id
    private Long queryGroupMemberId;
    private Long queryGroupId;
    private Long authUserId;
    private LocalDateTime joinedAt;
    private Long invitedByAuthUserId;
}
"""

    # Query Group Record Entity
    QUERY_GROUP_RECORD_ENTITY = """package {{ packageName }};

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("query_group_record")
public class QueryGroupRecord {
    
    @Id
    private Long queryGroupRecordId;
    private Long queryGroupId;
    private String tableName;
    private Long recordId;
    private Long addedByAuthUserId;
    private LocalDateTime addedAt;
}
"""

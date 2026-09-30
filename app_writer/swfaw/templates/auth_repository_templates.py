"""Authentication repository templates for code generation."""


class AuthRepositoryTemplates:
    """Templates for authentication/authorization repository generation."""
    
    # System Config Repository
    SYSTEM_CONFIG_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.SystemConfig;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;

@Repository
public interface SystemConfigRepository extends R2dbcRepository<SystemConfig, String> {
    
    Mono<SystemConfig> findByConfigKey(String configKey);
}
"""

    # Auth User Repository
    AUTH_USER_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.AuthUser;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

@Repository
public interface AuthUserRepository extends R2dbcRepository<AuthUser, Long> {
    
    Mono<AuthUser> findByUsername(String username);
    Mono<AuthUser> findByEmail(String email);
    Flux<AuthUser> findByIsActive(Boolean isActive);
    Mono<Boolean> existsByUsername(String username);
    Mono<Boolean> existsByEmail(String email);
}
"""

    # Access Audit Log Repository
    ACCESS_AUDIT_LOG_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.AccessAuditLog;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import java.time.LocalDateTime;

@Repository
public interface AccessAuditLogRepository extends R2dbcRepository<AccessAuditLog, Long> {
    
    Flux<AccessAuditLog> findByAuthUserId(Long authUserId);
    Flux<AccessAuditLog> findByTableNameAndRecordId(String tableName, Long recordId);
    Flux<AccessAuditLog> findByAccessGranted(Boolean accessGranted);
    Flux<AccessAuditLog> findByAuthUserIdAndAccessedAtBetween(Long authUserId, LocalDateTime start, LocalDateTime end);
}
"""

    # User Role Repository
    USER_ROLE_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.UserRole;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface UserRoleRepository extends R2dbcRepository<UserRole, Long> {
    
    Flux<UserRole> findByAuthUserId(Long authUserId);
    Flux<UserRole> findByAuthUserIdAndTableName(Long authUserId, String tableName);
    Flux<UserRole> findByRole(String role);
    Mono<Void> deleteByAuthUserIdAndTableName(Long authUserId, String tableName);
}
"""

    # Record Owner Repository
    RECORD_OWNER_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.RecordOwner;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface RecordOwnerRepository extends R2dbcRepository<RecordOwner, Long> {
    
    Flux<RecordOwner> findByAuthUserIdAndTableName(Long authUserId, String tableName);
    Flux<RecordOwner> findByTableNameAndRecordId(String tableName, Long recordId);
    @org.springframework.data.r2dbc.repository.Query("DELETE FROM record_owner WHERE table_name = :tableName AND record_id = :recordId")
    Mono<Void> deleteByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Boolean> existsByAuthUserIdAndTableNameAndRecordId(Long authUserId, String tableName, Long recordId);
}
"""

    # Query Group Repository
    QUERY_GROUP_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.QueryGroup;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupRepository extends R2dbcRepository<QueryGroup, Long> {
    
    Flux<QueryGroup> findByGroupType(String groupType);
    Flux<QueryGroup> findByOwnerAuthUserId(Long ownerAuthUserId);
    Mono<QueryGroup> findByGroupName(String groupName);
}
"""

    # Query Group Query Repository
    QUERY_GROUP_QUERY_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.QueryGroupQuery;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;

@Repository
public interface QueryGroupQueryRepository extends R2dbcRepository<QueryGroupQuery, Long> {
    
    Flux<QueryGroupQuery> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupQuery> findByQueryName(String queryName);
}
"""

    # Query Group Member Repository
    QUERY_GROUP_MEMBER_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.QueryGroupMember;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupMemberRepository extends R2dbcRepository<QueryGroupMember, Long> {
    
    Flux<QueryGroupMember> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupMember> findByAuthUserId(Long authUserId);
    Mono<Boolean> existsByQueryGroupIdAndAuthUserId(Long queryGroupId, Long authUserId);
}
"""

    # Query Group Record Repository
    QUERY_GROUP_RECORD_REPOSITORY = """package {{ packageName }};

import {{ entityPackage }}.QueryGroupRecord;
import org.springframework.data.r2dbc.repository.R2dbcRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface QueryGroupRecordRepository extends R2dbcRepository<QueryGroupRecord, Long> {
    
    Flux<QueryGroupRecord> findByQueryGroupId(Long queryGroupId);
    Flux<QueryGroupRecord> findByTableNameAndRecordId(String tableName, Long recordId);
    Mono<Boolean> existsByQueryGroupIdAndTableNameAndRecordId(Long queryGroupId, String tableName, Long recordId);
}
"""

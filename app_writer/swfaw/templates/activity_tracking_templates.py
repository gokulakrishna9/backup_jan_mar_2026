"""Activity tracking templates - templates for user activity tracking components."""


class ActivityTrackingTemplates:
    """Templates for activity tracking entities, repositories, and services."""
    
    @staticmethod
    def generate_crud_activity_log_entity(package_name: str) -> str:
        """Generate CrudActivityLog entity for tracking CRUD operations."""
        return f"""package {package_name}.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking CRUD operations on all entities.
 * Records create, read, update, and delete operations with full context.
 */
@Table("crud_activity_log")
public class CrudActivityLog {{
    
    @Id
    private Long id;
    
    @Column("user_id")
    private Long userId;
    
    @Column("username")
    private String username;
    
    @Column("entity_type")
    private String entityType;
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("operation")
    private String operation; // CREATE, READ, UPDATE, DELETE
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("user_agent")
    private String userAgent;
    
    @Column("changes_json")
    private String changesJson; // JSON of what changed (for UPDATE)
    
    @Column("success")
    private Boolean success;
    
    @Column("error_message")
    private String errorMessage;
    
    // Constructors
    public CrudActivityLog() {{
        this.timestamp = LocalDateTime.now();
        this.success = true;
    }}
    
    // Getters and Setters
    public Long getId() {{
        return id;
    }}
    
    public void setId(Long id) {{
        this.id = id;
    }}
    
    public Long getUserId() {{
        return userId;
    }}
    
    public void setUserId(Long userId) {{
        this.userId = userId;
    }}
    
    public String getUsername() {{
        return username;
    }}
    
    public void setUsername(String username) {{
        this.username = username;
    }}
    
    public String getEntityType() {{
        return entityType;
    }}
    
    public void setEntityType(String entityType) {{
        this.entityType = entityType;
    }}
    
    public Long getEntityId() {{
        return entityId;
    }}
    
    public void setEntityId(Long entityId) {{
        this.entityId = entityId;
    }}
    
    public String getOperation() {{
        return operation;
    }}
    
    public void setOperation(String operation) {{
        this.operation = operation;
    }}
    
    public LocalDateTime getTimestamp() {{
        return timestamp;
    }}
    
    public void setTimestamp(LocalDateTime timestamp) {{
        this.timestamp = timestamp;
    }}
    
    public String getIpAddress() {{
        return ipAddress;
    }}
    
    public void setIpAddress(String ipAddress) {{
        this.ipAddress = ipAddress;
    }}
    
    public String getUserAgent() {{
        return userAgent;
    }}
    
    public void setUserAgent(String userAgent) {{
        this.userAgent = userAgent;
    }}
    
    public String getChangesJson() {{
        return changesJson;
    }}
    
    public void setChangesJson(String changesJson) {{
        this.changesJson = changesJson;
    }}
    
    public Boolean getSuccess() {{
        return success;
    }}
    
    public void setSuccess(Boolean success) {{
        this.success = success;
    }}
    
    public String getErrorMessage() {{
        return errorMessage;
    }}
    
    public void setErrorMessage(String errorMessage) {{
        this.errorMessage = errorMessage;
    }}
}}
"""
    
    @staticmethod
    def generate_deleted_record_entity(package_name: str) -> str:
        """Generate DeletedRecord entity for storing deleted records as JSON."""
        return f"""package {package_name}.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for storing complete deleted records as JSON.
 * Allows recovery and audit of deleted data.
 */
@Table("deleted_record")
public class DeletedRecord {{
    
    @Id
    private Long id;
    
    @Column("entity_type")
    private String entityType;
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("record_json")
    private String recordJson; // Complete JSON of deleted record
    
    @Column("deleted_by_user_id")
    private Long deletedByUserId;
    
    @Column("deleted_by_username")
    private String deletedByUsername;
    
    @Column("deleted_at")
    private LocalDateTime deletedAt;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("reason")
    private String reason;
    
    @Column("can_restore")
    private Boolean canRestore;
    
    // Constructors
    public DeletedRecord() {{
        this.deletedAt = LocalDateTime.now();
        this.canRestore = true;
    }}
    
    // Getters and Setters
    public Long getId() {{
        return id;
    }}
    
    public void setId(Long id) {{
        this.id = id;
    }}
    
    public String getEntityType() {{
        return entityType;
    }}
    
    public void setEntityType(String entityType) {{
        this.entityType = entityType;
    }}
    
    public Long getEntityId() {{
        return entityId;
    }}
    
    public void setEntityId(Long entityId) {{
        this.entityId = entityId;
    }}
    
    public String getRecordJson() {{
        return recordJson;
    }}
    
    public void setRecordJson(String recordJson) {{
        this.recordJson = recordJson;
    }}
    
    public Long getDeletedByUserId() {{
        return deletedByUserId;
    }}
    
    public void setDeletedByUserId(Long deletedByUserId) {{
        this.deletedByUserId = deletedByUserId;
    }}
    
    public String getDeletedByUsername() {{
        return deletedByUsername;
    }}
    
    public void setDeletedByUsername(String deletedByUsername) {{
        this.deletedByUsername = deletedByUsername;
    }}
    
    public LocalDateTime getDeletedAt() {{
        return deletedAt;
    }}
    
    public void setDeletedAt(LocalDateTime deletedAt) {{
        this.deletedAt = deletedAt;
    }}
    
    public String getIpAddress() {{
        return ipAddress;
    }}
    
    public void setIpAddress(String ipAddress) {{
        this.ipAddress = ipAddress;
    }}
    
    public String getReason() {{
        return reason;
    }}
    
    public void setReason(String reason) {{
        this.reason = reason;
    }}
    
    public Boolean getCanRestore() {{
        return canRestore;
    }}
    
    public void setCanRestore(Boolean canRestore) {{
        this.canRestore = canRestore;
    }}
}}
"""
    
    @staticmethod
    def generate_login_activity_log_entity(package_name: str) -> str:
        """Generate LoginActivityLog entity for tracking login/logout events."""
        return f"""package {package_name}.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking user login and logout activities.
 * Records authentication events with session information.
 */
@Table("login_activity_log")
public class LoginActivityLog {{
    
    @Id
    private Long id;
    
    @Column("user_id")
    private Long userId;
    
    @Column("username")
    private String username;
    
    @Column("activity_type")
    private String activityType; // LOGIN, LOGOUT, LOGIN_FAILED
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("user_agent")
    private String userAgent;
    
    @Column("session_id")
    private String sessionId;
    
    @Column("success")
    private Boolean success;
    
    @Column("failure_reason")
    private String failureReason;
    
    @Column("login_method")
    private String loginMethod; // PASSWORD, OAUTH2, SAML
    
    @Column("oauth2_provider")
    private String oauth2Provider; // Google, GitHub, etc.
    
    // Constructors
    public LoginActivityLog() {{
        this.timestamp = LocalDateTime.now();
        this.success = true;
    }}
    
    // Getters and Setters
    public Long getId() {{
        return id;
    }}
    
    public void setId(Long id) {{
        this.id = id;
    }}
    
    public Long getUserId() {{
        return userId;
    }}
    
    public void setUserId(Long userId) {{
        this.userId = userId;
    }}
    
    public String getUsername() {{
        return username;
    }}
    
    public void setUsername(String username) {{
        this.username = username;
    }}
    
    public String getActivityType() {{
        return activityType;
    }}
    
    public void setActivityType(String activityType) {{
        this.activityType = activityType;
    }}
    
    public LocalDateTime getTimestamp() {{
        return timestamp;
    }}
    
    public void setTimestamp(LocalDateTime timestamp) {{
        this.timestamp = timestamp;
    }}
    
    public String getIpAddress() {{
        return ipAddress;
    }}
    
    public void setIpAddress(String ipAddress) {{
        this.ipAddress = ipAddress;
    }}
    
    public String getUserAgent() {{
        return userAgent;
    }}
    
    public void setUserAgent(String userAgent) {{
        this.userAgent = userAgent;
    }}
    
    public String getSessionId() {{
        return sessionId;
    }}
    
    public void setSessionId(String sessionId) {{
        this.sessionId = sessionId;
    }}
    
    public Boolean getSuccess() {{
        return success;
    }}
    
    public void setSuccess(Boolean success) {{
        this.success = success;
    }}
    
    public String getFailureReason() {{
        return failureReason;
    }}
    
    public void setFailureReason(String failureReason) {{
        this.failureReason = failureReason;
    }}
    
    public String getLoginMethod() {{
        return loginMethod;
    }}
    
    public void setLoginMethod(String loginMethod) {{
        this.loginMethod = loginMethod;
    }}
    
    public String getOauth2Provider() {{
        return oauth2Provider;
    }}
    
    public void setOauth2Provider(String oauth2Provider) {{
        this.oauth2Provider = oauth2Provider;
    }}
}}
"""
    
    @staticmethod
    def generate_grant_activity_log_entity(package_name: str) -> str:
        """Generate GrantActivityLog entity for tracking permission/grant changes."""
        return f"""package {package_name}.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;

/**
 * Entity for tracking permission and grant changes.
 * Records all authorization modifications including group memberships and access controls.
 */
@Table("grant_activity_log")
public class GrantActivityLog {{
    
    @Id
    private Long id;
    
    @Column("granted_by_user_id")
    private Long grantedByUserId;
    
    @Column("granted_by_username")
    private String grantedByUsername;
    
    @Column("target_user_id")
    private Long targetUserId;
    
    @Column("target_username")
    private String targetUsername;
    
    @Column("grant_type")
    private String grantType; // GROUP_MEMBERSHIP, ACCESS_CONTROL, DOCUMENT_PERMISSION, ROLE_CHANGE
    
    @Column("action")
    private String action; // GRANT, REVOKE, MODIFY
    
    @Column("entity_type")
    private String entityType; // UserGroup, AccessControl, DocumentPermission, etc.
    
    @Column("entity_id")
    private Long entityId;
    
    @Column("previous_value_json")
    private String previousValueJson;
    
    @Column("new_value_json")
    private String newValueJson;
    
    @Column("timestamp")
    private LocalDateTime timestamp;
    
    @Column("ip_address")
    private String ipAddress;
    
    @Column("reason")
    private String reason;
    
    // Constructors
    public GrantActivityLog() {{
        this.timestamp = LocalDateTime.now();
    }}
    
    // Getters and Setters
    public Long getId() {{
        return id;
    }}
    
    public void setId(Long id) {{
        this.id = id;
    }}
    
    public Long getGrantedByUserId() {{
        return grantedByUserId;
    }}
    
    public void setGrantedByUserId(Long grantedByUserId) {{
        this.grantedByUserId = grantedByUserId;
    }}
    
    public String getGrantedByUsername() {{
        return grantedByUsername;
    }}
    
    public void setGrantedByUsername(String grantedByUsername) {{
        this.grantedByUsername = grantedByUsername;
    }}
    
    public Long getTargetUserId() {{
        return targetUserId;
    }}
    
    public void setTargetUserId(Long targetUserId) {{
        this.targetUserId = targetUserId;
    }}
    
    public String getTargetUsername() {{
        return targetUsername;
    }}
    
    public void setTargetUsername(String targetUsername) {{
        this.targetUsername = targetUsername;
    }}
    
    public String getGrantType() {{
        return grantType;
    }}
    
    public void setGrantType(String grantType) {{
        this.grantType = grantType;
    }}
    
    public String getAction() {{
        return action;
    }}
    
    public void setAction(String action) {{
        this.action = action;
    }}
    
    public String getEntityType() {{
        return entityType;
    }}
    
    public void setEntityType(String entityType) {{
        this.entityType = entityType;
    }}
    
    public Long getEntityId() {{
        return entityId;
    }}
    
    public void setEntityId(Long entityId) {{
        this.entityId = entityId;
    }}
    
    public String getPreviousValueJson() {{
        return previousValueJson;
    }}
    
    public void setPreviousValueJson(String previousValueJson) {{
        this.previousValueJson = previousValueJson;
    }}
    
    public String getNewValueJson() {{
        return newValueJson;
    }}
    
    public void setNewValueJson(String newValueJson) {{
        this.newValueJson = newValueJson;
    }}
    
    public LocalDateTime getTimestamp() {{
        return timestamp;
    }}
    
    public void setTimestamp(LocalDateTime timestamp) {{
        this.timestamp = timestamp;
    }}
    
    public String getIpAddress() {{
        return ipAddress;
    }}
    
    public void setIpAddress(String ipAddress) {{
        this.ipAddress = ipAddress;
    }}
    
    public String getReason() {{
        return reason;
    }}
    
    public void setReason(String reason) {{
        this.reason = reason;
    }}
}}
"""

    
    @staticmethod
    def generate_crud_activity_log_repository(package_name: str) -> str:
        """Generate CrudActivityLogRepository."""
        return f"""package {package_name}.repository;

import {package_name}.entity.CrudActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for CrudActivityLog entity.
 */
@Repository
public interface CrudActivityLogRepository extends ReactiveCrudRepository<CrudActivityLog, Long> {{
    
    Flux<CrudActivityLog> findByUserId(Long userId);
    
    Flux<CrudActivityLog> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    Flux<CrudActivityLog> findByOperation(String operation);
    
    @Query("SELECT * FROM crud_activity_log WHERE user_id = :userId AND operation = :operation ORDER BY timestamp DESC LIMIT :limit")
    Flux<CrudActivityLog> findRecentByUserIdAndOperation(Long userId, String operation, int limit);
    
    @Query("SELECT * FROM crud_activity_log WHERE entity_type = :entityType ORDER BY timestamp DESC LIMIT :limit")
    Flux<CrudActivityLog> findRecentByEntityType(String entityType, int limit);
    
    @Query("SELECT * FROM crud_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<CrudActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
}}
"""
    
    @staticmethod
    def generate_deleted_record_repository(package_name: str) -> str:
        """Generate DeletedRecordRepository."""
        return f"""package {package_name}.repository;

import {package_name}.entity.DeletedRecord;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for DeletedRecord entity.
 */
@Repository
public interface DeletedRecordRepository extends ReactiveCrudRepository<DeletedRecord, Long> {{
    
    Flux<DeletedRecord> findByEntityType(String entityType);
    
    Mono<DeletedRecord> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    Flux<DeletedRecord> findByDeletedByUserId(Long deletedByUserId);
    
    @Query("SELECT * FROM deleted_record WHERE can_restore = true ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findAllRestorableRecords();
    
    @Query("SELECT * FROM deleted_record WHERE entity_type = :entityType AND can_restore = true ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findRestorableByEntityType(String entityType);
    
    @Query("SELECT * FROM deleted_record WHERE deleted_at >= :startTime AND deleted_at <= :endTime ORDER BY deleted_at DESC")
    Flux<DeletedRecord> findByDeletedAtBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
}}
"""
    
    @staticmethod
    def generate_login_activity_log_repository(package_name: str) -> str:
        """Generate LoginActivityLogRepository."""
        return f"""package {package_name}.repository;

import {package_name}.entity.LoginActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for LoginActivityLog entity.
 */
@Repository
public interface LoginActivityLogRepository extends ReactiveCrudRepository<LoginActivityLog, Long> {{
    
    Flux<LoginActivityLog> findByUserId(Long userId);
    
    Flux<LoginActivityLog> findByActivityType(String activityType);
    
    Flux<LoginActivityLog> findByUsername(String username);
    
    @Query("SELECT * FROM login_activity_log WHERE user_id = :userId ORDER BY timestamp DESC LIMIT :limit")
    Flux<LoginActivityLog> findRecentByUserId(Long userId, int limit);
    
    @Query("SELECT * FROM login_activity_log WHERE success = false ORDER BY timestamp DESC LIMIT :limit")
    Flux<LoginActivityLog> findRecentFailedLogins(int limit);
    
    @Query("SELECT * FROM login_activity_log WHERE username = :username AND success = false AND timestamp >= :since")
    Flux<LoginActivityLog> findFailedLoginsSince(String username, java.time.LocalDateTime since);
    
    @Query("SELECT * FROM login_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<LoginActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
    
    @Query("SELECT * FROM login_activity_log WHERE activity_type = 'LOGIN' AND success = true AND user_id = :userId ORDER BY timestamp DESC LIMIT 1")
    Mono<LoginActivityLog> findLastSuccessfulLogin(Long userId);
}}
"""
    
    @staticmethod
    def generate_grant_activity_log_repository(package_name: str) -> str:
        """Generate GrantActivityLogRepository."""
        return f"""package {package_name}.repository;

import {package_name}.entity.GrantActivityLog;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * Repository for GrantActivityLog entity.
 */
@Repository
public interface GrantActivityLogRepository extends ReactiveCrudRepository<GrantActivityLog, Long> {{
    
    Flux<GrantActivityLog> findByTargetUserId(Long targetUserId);
    
    Flux<GrantActivityLog> findByGrantedByUserId(Long grantedByUserId);
    
    Flux<GrantActivityLog> findByGrantType(String grantType);
    
    @Query("SELECT * FROM grant_activity_log WHERE target_user_id = :userId ORDER BY timestamp DESC LIMIT :limit")
    Flux<GrantActivityLog> findRecentByTargetUserId(Long userId, int limit);
    
    @Query("SELECT * FROM grant_activity_log WHERE entity_type = :entityType AND entity_id = :entityId ORDER BY timestamp DESC")
    Flux<GrantActivityLog> findByEntityTypeAndEntityId(String entityType, Long entityId);
    
    @Query("SELECT * FROM grant_activity_log WHERE timestamp >= :startTime AND timestamp <= :endTime ORDER BY timestamp DESC")
    Flux<GrantActivityLog> findByTimestampBetween(java.time.LocalDateTime startTime, java.time.LocalDateTime endTime);
    
    @Query("SELECT * FROM grant_activity_log WHERE action = :action ORDER BY timestamp DESC LIMIT :limit")
    Flux<GrantActivityLog> findRecentByAction(String action, int limit);
}}
"""
    
    @staticmethod
    def generate_activity_tracking_service(package_name: str) -> str:
        """Generate ActivityTrackingService."""
        return f"""package {package_name}.service;

import {package_name}.entity.*;
import {package_name}.repository.*;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

import java.time.LocalDateTime;

/**
 * Service for tracking user activities including CRUD operations, logins, and grants.
 */
@Service
public class ActivityTrackingService {{
    
    private final CrudActivityLogRepository crudActivityLogRepository;
    private final DeletedRecordRepository deletedRecordRepository;
    private final LoginActivityLogRepository loginActivityLogRepository;
    private final GrantActivityLogRepository grantActivityLogRepository;
    private final ObjectMapper objectMapper;
    
    public ActivityTrackingService(
            CrudActivityLogRepository crudActivityLogRepository,
            DeletedRecordRepository deletedRecordRepository,
            LoginActivityLogRepository loginActivityLogRepository,
            GrantActivityLogRepository grantActivityLogRepository,
            ObjectMapper objectMapper) {{
        this.crudActivityLogRepository = crudActivityLogRepository;
        this.deletedRecordRepository = deletedRecordRepository;
        this.loginActivityLogRepository = loginActivityLogRepository;
        this.grantActivityLogRepository = grantActivityLogRepository;
        this.objectMapper = objectMapper;
    }}
    
    // CRUD Activity Tracking
    
    public Mono<Void> logCreate(Long userId, String username, String entityType, Long entityId, 
                                 String ipAddress, String userAgent) {{
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("CREATE");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        
        return crudActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logRead(Long userId, String username, String entityType, Long entityId,
                              String ipAddress, String userAgent) {{
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("READ");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        
        return crudActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logUpdate(Long userId, String username, String entityType, Long entityId,
                                String changesJson, String ipAddress, String userAgent) {{
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("UPDATE");
        log.setChangesJson(changesJson);
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        
        return crudActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logDelete(Long userId, String username, String entityType, Long entityId,
                                Object deletedRecord, String ipAddress, String reason) {{
        // Log the delete operation
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("DELETE");
        log.setIpAddress(ipAddress);
        
        // Store the deleted record as JSON
        DeletedRecord deletedRecordEntity = new DeletedRecord();
        deletedRecordEntity.setEntityType(entityType);
        deletedRecordEntity.setEntityId(entityId);
        deletedRecordEntity.setDeletedByUserId(userId);
        deletedRecordEntity.setDeletedByUsername(username);
        deletedRecordEntity.setIpAddress(ipAddress);
        deletedRecordEntity.setReason(reason);
        
        try {{
            String recordJson = objectMapper.writeValueAsString(deletedRecord);
            deletedRecordEntity.setRecordJson(recordJson);
        }} catch (Exception e) {{
            deletedRecordEntity.setRecordJson("{{\\\"error\\\": \\\"Failed to serialize record\\\"}}");
        }}
        
        return Mono.zip(
            crudActivityLogRepository.save(log),
            deletedRecordRepository.save(deletedRecordEntity)
        ).then();
    }}
    
    public Mono<Void> logFailedOperation(Long userId, String username, String entityType, 
                                         Long entityId, String operation, String errorMessage,
                                         String ipAddress) {{
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation(operation);
        log.setSuccess(false);
        log.setErrorMessage(errorMessage);
        log.setIpAddress(ipAddress);
        
        return crudActivityLogRepository.save(log).then();
    }}
    
    // Login Activity Tracking
    
    public Mono<Void> logLogin(Long userId, String username, String ipAddress, String userAgent,
                               String sessionId, String loginMethod, String oauth2Provider) {{
        LoginActivityLog log = new LoginActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setActivityType("LOGIN");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        log.setSessionId(sessionId);
        log.setLoginMethod(loginMethod);
        log.setOauth2Provider(oauth2Provider);
        
        return loginActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logLogout(Long userId, String username, String ipAddress, String sessionId) {{
        LoginActivityLog log = new LoginActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setActivityType("LOGOUT");
        log.setIpAddress(ipAddress);
        log.setSessionId(sessionId);
        
        return loginActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logFailedLogin(String username, String ipAddress, String userAgent,
                                     String failureReason, String loginMethod) {{
        LoginActivityLog log = new LoginActivityLog();
        log.setUsername(username);
        log.setActivityType("LOGIN_FAILED");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        log.setSuccess(false);
        log.setFailureReason(failureReason);
        log.setLoginMethod(loginMethod);
        
        return loginActivityLogRepository.save(log).then();
    }}
    
    // Grant Activity Tracking
    
    public Mono<Void> logGrant(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                               String targetUsername, String grantType, String entityType, Long entityId,
                               Object previousValue, Object newValue, String ipAddress, String reason) {{
        GrantActivityLog log = new GrantActivityLog();
        log.setGrantedByUserId(grantedByUserId);
        log.setGrantedByUsername(grantedByUsername);
        log.setTargetUserId(targetUserId);
        log.setTargetUsername(targetUsername);
        log.setGrantType(grantType);
        log.setAction("GRANT");
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setIpAddress(ipAddress);
        log.setReason(reason);
        
        try {{
            if (previousValue != null) {{
                log.setPreviousValueJson(objectMapper.writeValueAsString(previousValue));
            }}
            if (newValue != null) {{
                log.setNewValueJson(objectMapper.writeValueAsString(newValue));
            }}
        }} catch (Exception e) {{
            // Ignore serialization errors
        }}
        
        return grantActivityLogRepository.save(log).then();
    }}
    
    public Mono<Void> logRevoke(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                                String targetUsername, String grantType, String entityType, Long entityId,
                                Object previousValue, String ipAddress, String reason) {{
        GrantActivityLog log = new GrantActivityLog();
        log.setGrantedByUserId(grantedByUserId);
        log.setGrantedByUsername(grantedByUsername);
        log.setTargetUserId(targetUserId);
        log.setTargetUsername(targetUsername);
        log.setGrantType(grantType);
        log.setAction("REVOKE");
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setIpAddress(ipAddress);
        log.setReason(reason);
        
        try {{
            if (previousValue != null) {{
                log.setPreviousValueJson(objectMapper.writeValueAsString(previousValue));
            }}
        }} catch (Exception e) {{
            // Ignore serialization errors
        }}
        
        return grantActivityLogRepository.save(log).then();
    }}
    
    // Query Methods
    
    public Flux<CrudActivityLog> getUserCrudActivity(Long userId, int limit) {{
        return crudActivityLogRepository.findRecentByUserIdAndOperation(userId, null, limit);
    }}
    
    public Flux<CrudActivityLog> getEntityHistory(String entityType, Long entityId) {{
        return crudActivityLogRepository.findByEntityTypeAndEntityId(entityType, entityId);
    }}
    
    public Flux<LoginActivityLog> getUserLoginHistory(Long userId, int limit) {{
        return loginActivityLogRepository.findRecentByUserId(userId, limit);
    }}
    
    public Flux<GrantActivityLog> getUserGrantHistory(Long userId, int limit) {{
        return grantActivityLogRepository.findRecentByTargetUserId(userId, limit);
    }}
    
    public Flux<DeletedRecord> getRestorableRecords(String entityType) {{
        if (entityType != null) {{
            return deletedRecordRepository.findRestorableByEntityType(entityType);
        }}
        return deletedRecordRepository.findAllRestorableRecords();
    }}
    
    public Mono<DeletedRecord> getDeletedRecord(String entityType, Long entityId) {{
        return deletedRecordRepository.findByEntityTypeAndEntityId(entityType, entityId);
    }}
    
    // Helper method to extract IP address from exchange
    public String getIpAddress(ServerWebExchange exchange) {{
        String ip = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
        if (ip == null || ip.isEmpty()) {{
            ip = exchange.getRequest().getRemoteAddress() != null 
                ? exchange.getRequest().getRemoteAddress().getAddress().getHostAddress() 
                : "unknown";
        }}
        return ip;
    }}
    
    // Helper method to extract user agent from exchange
    public String getUserAgent(ServerWebExchange exchange) {{
        return exchange.getRequest().getHeaders().getFirst("User-Agent");
    }}
}}
"""

    
    @staticmethod
    def generate_activity_tracking_controller(package_name: str) -> str:
        """Generate ActivityTrackingController for querying activity logs."""
        return f"""package {package_name}.controller;

import {package_name}.entity.*;
import {package_name}.service.ActivityTrackingService;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * REST controller for querying activity tracking logs.
 * Provides endpoints for viewing CRUD, login, and grant activities.
 */
@RestController
@RequestMapping("/api/activity")
public class ActivityTrackingController {{
    
    private final ActivityTrackingService activityTrackingService;
    
    public ActivityTrackingController(ActivityTrackingService activityTrackingService) {{
        this.activityTrackingService = activityTrackingService;
    }}
    
    /**
     * Get CRUD activity for a specific user.
     */
    @GetMapping("/crud/user/{{userId}}")
    public Flux<CrudActivityLog> getUserCrudActivity(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "100") int limit) {{
        return activityTrackingService.getUserCrudActivity(userId, limit);
    }}
    
    /**
     * Get complete history for a specific entity.
     */
    @GetMapping("/crud/entity/{{entityType}}/{{entityId}}")
    public Flux<CrudActivityLog> getEntityHistory(
            @PathVariable String entityType,
            @PathVariable Long entityId) {{
        return activityTrackingService.getEntityHistory(entityType, entityId);
    }}
    
    /**
     * Get login history for a specific user.
     */
    @GetMapping("/login/user/{{userId}}")
    public Flux<LoginActivityLog> getUserLoginHistory(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "50") int limit) {{
        return activityTrackingService.getUserLoginHistory(userId, limit);
    }}
    
    /**
     * Get grant/permission history for a specific user.
     */
    @GetMapping("/grant/user/{{userId}}")
    public Flux<GrantActivityLog> getUserGrantHistory(
            @PathVariable Long userId,
            @RequestParam(defaultValue = "50") int limit) {{
        return activityTrackingService.getUserGrantHistory(userId, limit);
    }}
    
    /**
     * Get all restorable deleted records.
     */
    @GetMapping("/deleted")
    public Flux<DeletedRecord> getRestorableRecords(
            @RequestParam(required = false) String entityType) {{
        return activityTrackingService.getRestorableRecords(entityType);
    }}
    
    /**
     * Get a specific deleted record.
     */
    @GetMapping("/deleted/{{entityType}}/{{entityId}}")
    public Mono<ResponseEntity<DeletedRecord>> getDeletedRecord(
            @PathVariable String entityType,
            @PathVariable Long entityId) {{
        return activityTrackingService.getDeletedRecord(entityType, entityId)
                .map(ResponseEntity::ok)
                .defaultIfEmpty(ResponseEntity.notFound().build());
    }}
}}
"""
    
    # SQL Schema for activity tracking tables
    ACTIVITY_TRACKING_SCHEMA_SQL = """-- Activity Tracking Schema
-- Tables for tracking user activities: CRUD operations, logins, and grants

-- Table: crud_activity_log
-- Tracks all CRUD operations on entities
CREATE TABLE IF NOT EXISTS crud_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    username VARCHAR(255),
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT,
    operation VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    changes_json TEXT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    INDEX idx_user_id (user_id),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_operation (operation),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: deleted_record
-- Stores complete deleted records as JSON for recovery
CREATE TABLE IF NOT EXISTS deleted_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    record_json LONGTEXT NOT NULL,
    deleted_by_user_id BIGINT,
    deleted_by_username VARCHAR(255),
    deleted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    reason TEXT,
    can_restore BOOLEAN DEFAULT TRUE,
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_deleted_by (deleted_by_user_id),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_can_restore (can_restore)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: login_activity_log
-- Tracks login and logout events
CREATE TABLE IF NOT EXISTS login_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    username VARCHAR(255),
    activity_type VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(255),
    success BOOLEAN DEFAULT TRUE,
    failure_reason TEXT,
    login_method VARCHAR(50),
    oauth2_provider VARCHAR(50),
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_activity_type (activity_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_success (success)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: grant_activity_log
-- Tracks permission and grant changes
CREATE TABLE IF NOT EXISTS grant_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    granted_by_user_id BIGINT,
    granted_by_username VARCHAR(255),
    target_user_id BIGINT,
    target_username VARCHAR(255),
    grant_type VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_type VARCHAR(100),
    entity_id BIGINT,
    previous_value_json TEXT,
    new_value_json TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    reason TEXT,
    INDEX idx_granted_by (granted_by_user_id),
    INDEX idx_target_user (target_user_id),
    INDEX idx_grant_type (grant_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_entity (entity_type, entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
"""

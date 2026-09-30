package com.example.service;

import com.example.entity.*;
import com.example.repository.*;
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
public class ActivityTrackingService {
    
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
            ObjectMapper objectMapper) {
        this.crudActivityLogRepository = crudActivityLogRepository;
        this.deletedRecordRepository = deletedRecordRepository;
        this.loginActivityLogRepository = loginActivityLogRepository;
        this.grantActivityLogRepository = grantActivityLogRepository;
        this.objectMapper = objectMapper;
    }
    
    // CRUD Activity Tracking
    
    public Mono<Void> logCreate(Long userId, String username, String entityType, Long entityId, 
                                 String ipAddress, String userAgent) {
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("CREATE");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        
        return crudActivityLogRepository.save(log).then();
    }
    
    public Mono<Void> logRead(Long userId, String username, String entityType, Long entityId,
                              String ipAddress, String userAgent) {
        CrudActivityLog log = new CrudActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setEntityType(entityType);
        log.setEntityId(entityId);
        log.setOperation("READ");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        
        return crudActivityLogRepository.save(log).then();
    }
    
    public Mono<Void> logUpdate(Long userId, String username, String entityType, Long entityId,
                                String changesJson, String ipAddress, String userAgent) {
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
    }
    
    public Mono<Void> logDelete(Long userId, String username, String entityType, Long entityId,
                                Object deletedRecord, String ipAddress, String reason) {
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
        
        try {
            String recordJson = objectMapper.writeValueAsString(deletedRecord);
            deletedRecordEntity.setRecordJson(recordJson);
        } catch (Exception e) {
            deletedRecordEntity.setRecordJson("{\"error\": \"Failed to serialize record\"}");
        }
        
        return Mono.zip(
            crudActivityLogRepository.save(log),
            deletedRecordRepository.save(deletedRecordEntity)
        ).then();
    }
    
    public Mono<Void> logFailedOperation(Long userId, String username, String entityType, 
                                         Long entityId, String operation, String errorMessage,
                                         String ipAddress) {
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
    }
    
    // Login Activity Tracking
    
    public Mono<Void> logLogin(Long userId, String username, String ipAddress, String userAgent,
                               String sessionId, String loginMethod, String oauth2Provider) {
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
    }
    
    public Mono<Void> logLogout(Long userId, String username, String ipAddress, String sessionId) {
        LoginActivityLog log = new LoginActivityLog();
        log.setUserId(userId);
        log.setUsername(username);
        log.setActivityType("LOGOUT");
        log.setIpAddress(ipAddress);
        log.setSessionId(sessionId);
        
        return loginActivityLogRepository.save(log).then();
    }
    
    public Mono<Void> logFailedLogin(String username, String ipAddress, String userAgent,
                                     String failureReason, String loginMethod) {
        LoginActivityLog log = new LoginActivityLog();
        log.setUsername(username);
        log.setActivityType("LOGIN_FAILED");
        log.setIpAddress(ipAddress);
        log.setUserAgent(userAgent);
        log.setSuccess(false);
        log.setFailureReason(failureReason);
        log.setLoginMethod(loginMethod);
        
        return loginActivityLogRepository.save(log).then();
    }
    
    // Grant Activity Tracking
    
    public Mono<Void> logGrant(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                               String targetUsername, String grantType, String entityType, Long entityId,
                               Object previousValue, Object newValue, String ipAddress, String reason) {
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
        
        try {
            if (previousValue != null) {
                log.setPreviousValueJson(objectMapper.writeValueAsString(previousValue));
            }
            if (newValue != null) {
                log.setNewValueJson(objectMapper.writeValueAsString(newValue));
            }
        } catch (Exception e) {
            // Ignore serialization errors
        }
        
        return grantActivityLogRepository.save(log).then();
    }
    
    public Mono<Void> logRevoke(Long grantedByUserId, String grantedByUsername, Long targetUserId,
                                String targetUsername, String grantType, String entityType, Long entityId,
                                Object previousValue, String ipAddress, String reason) {
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
        
        try {
            if (previousValue != null) {
                log.setPreviousValueJson(objectMapper.writeValueAsString(previousValue));
            }
        } catch (Exception e) {
            // Ignore serialization errors
        }
        
        return grantActivityLogRepository.save(log).then();
    }
    
    // Query Methods
    
    public Flux<CrudActivityLog> getUserCrudActivity(Long userId, int limit) {
        return crudActivityLogRepository.findRecentByUserIdAndOperation(userId, null, limit);
    }
    
    public Flux<CrudActivityLog> getEntityHistory(String entityType, Long entityId) {
        return crudActivityLogRepository.findByEntityTypeAndEntityId(entityType, entityId);
    }
    
    public Flux<LoginActivityLog> getUserLoginHistory(Long userId, int limit) {
        return loginActivityLogRepository.findRecentByUserId(userId, limit);
    }
    
    public Flux<GrantActivityLog> getUserGrantHistory(Long userId, int limit) {
        return grantActivityLogRepository.findRecentByTargetUserId(userId, limit);
    }
    
    public Flux<DeletedRecord> getRestorableRecords(String entityType) {
        if (entityType != null) {
            return deletedRecordRepository.findRestorableByEntityType(entityType);
        }
        return deletedRecordRepository.findAllRestorableRecords();
    }
    
    public Mono<DeletedRecord> getDeletedRecord(String entityType, Long entityId) {
        return deletedRecordRepository.findByEntityTypeAndEntityId(entityType, entityId);
    }
    
    // Helper method to extract IP address from exchange
    public String getIpAddress(ServerWebExchange exchange) {
        String ip = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
        if (ip == null || ip.isEmpty()) {
            ip = exchange.getRequest().getRemoteAddress() != null 
                ? exchange.getRequest().getRemoteAddress().getAddress().getHostAddress() 
                : "unknown";
        }
        return ip;
    }
    
    // Helper method to extract user agent from exchange
    public String getUserAgent(ServerWebExchange exchange) {
        return exchange.getRequest().getHeaders().getFirst("User-Agent");
    }
}

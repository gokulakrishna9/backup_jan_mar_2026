package com.example.service;

import com.example.entity.AccessAuditLog;
import com.example.entity.AuthUser;
import com.example.repository.AccessAuditLogRepository;
import com.example.repository.AuthUserRepository;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;

/**
 * Service for audit logging of access attempts
 */
@Slf4j
@Service
@RequiredArgsConstructor
public class AuditLoggingService {
    
    private final AccessAuditLogRepository accessAuditLogRepository;
    private final AuthUserRepository authUserRepository;
    
    /**
     * Log an access attempt (granted or denied)
     */
    public Mono<Void> logAccessAttempt(
            Long authUserId,
            String tableName,
            Long recordId,
            String accessControl,
            boolean granted,
            String reason) {
        
        AccessAuditLog auditLog = new AccessAuditLog();
        auditLog.setAuthUserId(authUserId);
        auditLog.setAction(accessControl);
        auditLog.setTableName(tableName);
        auditLog.setRecordId(recordId);
        auditLog.setAccessGranted(granted);
        auditLog.setDenialReason(granted ? null : reason);
        auditLog.setAccessedAt(LocalDateTime.now());
        
        return accessAuditLogRepository.save(auditLog)
            .doOnSuccess(saved -> 
                log.debug("Access audit logged: user={}, table={}, record={}, control={}, granted={}", 
                    authUserId, tableName, recordId, accessControl, granted)
            )
            .doOnError(error -> 
                log.error("Failed to log access audit", error)
            )
            .then();
    }
    
    /**
     * Get access audit logs for a user
     */
    public Mono<java.util.List<AccessAuditLog>> getAccessAuditLogs(
            Long authUserId,
            LocalDateTime startTime,
            LocalDateTime endTime) {
        
        return accessAuditLogRepository.findByAuthUserId(authUserId)
            .filter(log -> !log.getAccessedAt().isBefore(startTime) && !log.getAccessedAt().isAfter(endTime))
            .collectList();
    }
    
    /**
     * Get all access audit logs for a specific record
     */
    public Mono<java.util.List<AccessAuditLog>> getRecordAccessLogs(
            String tableName,
            Long recordId) {
        
        return accessAuditLogRepository.findByTableNameAndRecordId(tableName, recordId)
            .collectList();
    }
    
    /**
     * Get denied access attempts for security monitoring
     */
    public Mono<java.util.List<AccessAuditLog>> getDeniedAccessAttempts(
            LocalDateTime startTime,
            LocalDateTime endTime) {
        
        return accessAuditLogRepository.findByAccessGranted(false)
            .filter(log -> !log.getAccessedAt().isBefore(startTime) && !log.getAccessedAt().isAfter(endTime))
            .collectList();
    }
}
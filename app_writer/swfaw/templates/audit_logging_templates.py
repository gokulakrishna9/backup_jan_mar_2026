"""Audit logging service templates for tracking access attempts."""


class AuditLoggingTemplates:
    """Templates for audit logging service generation."""
    
    # Audit Logging Service
    AUDIT_LOGGING_SERVICE = """package {{ packageName }};

import {{ entityPackage }}.AccessAuditLog;
import {{ entityPackage }}.AuthUser;
import {{ repositoryPackage }}.AccessAuditLogRepository;
import {{ repositoryPackage }}.AuthUserRepository;
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
"""

    # Audit Controller for viewing logs
    AUDIT_CONTROLLER = """package {{ packageName }};

import {{ servicePackage }}.AuditLoggingService;
import {{ entityPackage }}.AccessAuditLog;
import {{ securityPackage }}.SecurityContextHolder;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;
import java.util.List;

/**
 * Controller for viewing audit logs
 * Requires admin access
 */
@RestController
@RequestMapping("/api/audit")
@RequiredArgsConstructor
public class AuditController {
    
    private final AuditLoggingService auditLoggingService;
    
    /**
     * Get access audit logs for current user
     */
    @GetMapping("/access-logs/me")
    public Mono<ResponseEntity<List<AccessAuditLog>>> getMyAccessLogs(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startTime,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endTime) {
        
        return SecurityContextHolder.getCurrentUser()
            .flatMap(user -> auditLoggingService.getAccessAuditLogs(
                user.getAuthUserId(), startTime, endTime
            ))
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }
    
    /**
     * Get access audit logs for a specific user (admin only)
     */
    @GetMapping("/access-logs/user/{userId}")
    public Mono<ResponseEntity<List<AccessAuditLog>>> getUserAccessLogs(
            @PathVariable Long userId,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startTime,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endTime) {
        
        // TODO: Add admin authorization check
        return auditLoggingService.getAccessAuditLogs(userId, startTime, endTime)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }
    
    /**
     * Get all access logs for a specific record (admin only)
     */
    @GetMapping("/access-logs/record")
    public Mono<ResponseEntity<List<AccessAuditLog>>> getRecordAccessLogs(
            @RequestParam String tableName,
            @RequestParam Long recordId) {
        
        // TODO: Add admin authorization check
        return auditLoggingService.getRecordAccessLogs(tableName, recordId)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }
    
    /**
     * Get denied access attempts for security monitoring (admin only)
     */
    @GetMapping("/denied-access")
    public Mono<ResponseEntity<List<AccessAuditLog>>> getDeniedAccessAttempts(
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime startTime,
            @RequestParam @DateTimeFormat(iso = DateTimeFormat.ISO.DATE_TIME) LocalDateTime endTime) {
        
        // TODO: Add admin authorization check
        return auditLoggingService.getDeniedAccessAttempts(startTime, endTime)
            .map(ResponseEntity::ok)
            .defaultIfEmpty(ResponseEntity.notFound().build());
    }
}
"""

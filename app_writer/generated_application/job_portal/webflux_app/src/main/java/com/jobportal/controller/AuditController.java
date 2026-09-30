package com.jobportal.controller;

import com.jobportal.service.AuditLoggingService;
import com.jobportal.entity.AccessAuditLog;
import com.jobportal.security.SecurityContextHolder;
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
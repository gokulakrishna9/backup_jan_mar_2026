package com.example.repository;

import com.example.entity.AccessAuditLog;
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
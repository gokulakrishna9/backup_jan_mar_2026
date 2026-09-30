package com.example.entity;

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
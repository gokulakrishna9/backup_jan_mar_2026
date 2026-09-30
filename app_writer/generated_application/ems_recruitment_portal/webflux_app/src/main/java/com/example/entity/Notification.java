package com.example.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Entity class for ems_notification table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_notification")
public class Notification {
    
    @Id
    @Column("notification_id")
    private Long notificationId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("notification_type")
    private String notificationType;
    
    @Column("title")
    private String title;
    
    @Column("message")
    private String message;
    
    @Column("related_entity_type")
    private String relatedEntityType;
    
    @Column("related_entity_id")
    private Long relatedEntityId;
    
    @Column("action_url")
    private String actionUrl;
    
    @Column("is_read")
    private Byte isRead;
    
    @Column("read_at")
    private LocalDateTime readAt;
    
    @Column("priority")
    private String priority;
    
}
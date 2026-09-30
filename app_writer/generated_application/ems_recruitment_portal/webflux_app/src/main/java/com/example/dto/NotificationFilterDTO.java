package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for Notification search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NotificationFilterDTO {
    
    // Filter type: EQUALS
    private Long notificationId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String notificationType;
    
    // Filter type: LIKE
    private String title;
    
    // Filter type: LIKE
    private String message;
    
    // Filter type: LIKE
    private String relatedEntityType;
    
    // Filter type: EQUALS
    private Long relatedEntityId;
    
    // Filter type: LIKE
    private String actionUrl;
    
    // Filter type: EQUALS
    private LocalDateTime readAt;
    
    // Filter type: LIKE
    private String priority;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
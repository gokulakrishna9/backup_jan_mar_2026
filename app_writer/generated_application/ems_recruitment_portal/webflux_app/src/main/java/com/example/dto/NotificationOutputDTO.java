package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Notification responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class NotificationOutputDTO {
    
    private Long notificationId;
    
    private Long userId;
    
    private String notificationType;
    
    private String title;
    
    private String message;
    
    private String relatedEntityType;
    
    private Long relatedEntityId;
    
    private String actionUrl;
    
    private Byte isRead;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime readAt;
    
    private String priority;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
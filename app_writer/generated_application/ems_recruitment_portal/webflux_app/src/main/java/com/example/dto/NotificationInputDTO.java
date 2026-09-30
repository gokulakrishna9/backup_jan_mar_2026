package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for Notification creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class NotificationInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Notificationtype is required")
    @Size(max = 100, message = "Notificationtype cannot exceed 100 characters")
    private String notificationType;
    
    @NotNull(message = "Title is required")
    @Size(max = 255, message = "Title cannot exceed 255 characters")
    private String title;
    
    @NotNull(message = "Message is required")
    private String message;
    
    @Size(max = 100, message = "Relatedentitytype cannot exceed 100 characters")
    private String relatedEntityType;
    
    private Long relatedEntityId;
    
    @Size(max = 500, message = "Actionurl cannot exceed 500 characters")
    private String actionUrl;
    
    private Byte isRead;
    
    private LocalDateTime readAt;
    
    private String priority;
    
}
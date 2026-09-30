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
 * Output DTO for UserAchievement responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserAchievementOutputDTO {
    
    private Long achievementId;
    
    private Long userId;
    
    private String title;
    
    private String description;
    
    private String achievementType;
    
    private String issuer;
    
    // Format: yyyy-MM-dd
    private LocalDate dateAchieved;
    
    private String url;
    
    private Long documentId;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
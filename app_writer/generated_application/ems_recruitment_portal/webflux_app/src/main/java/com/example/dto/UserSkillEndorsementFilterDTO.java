package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserSkillEndorsement search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSkillEndorsementFilterDTO {
    
    // Filter type: EQUALS
    private Long endorsementId;
    
    // Filter type: EQUALS
    private Long skillId;
    
    // Filter type: EQUALS
    private Long endorsedByUserId;
    
    // Filter type: LIKE
    private String endorsementComment;
    
    // Filter type: LIKE
    private String relationship;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
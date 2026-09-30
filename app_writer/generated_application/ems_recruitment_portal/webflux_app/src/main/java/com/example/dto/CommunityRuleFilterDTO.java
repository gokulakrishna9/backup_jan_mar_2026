package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityRule search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityRuleFilterDTO {
    
    // Filter type: EQUALS
    private Long ruleId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: LIKE
    private String ruleTitle;
    
    // Filter type: LIKE
    private String ruleDescription;
    
    // Filter type: EQUALS
    private Integer orderSequence;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
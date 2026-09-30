package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityCategory search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityCategoryFilterDTO {
    
    // Filter type: EQUALS
    private Long categoryId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: LIKE
    private String categoryName;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String icon;
    
    // Filter type: LIKE
    private String color;
    
    // Filter type: EQUALS
    private Integer orderSequence;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
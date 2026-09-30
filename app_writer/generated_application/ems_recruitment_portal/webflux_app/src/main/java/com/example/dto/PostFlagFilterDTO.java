package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for PostFlag search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostFlagFilterDTO {
    
    // Filter type: EQUALS
    private Long flagId;
    
    // Filter type: LIKE
    private String type;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: LIKE
    private String reason;
    
    // Filter type: EQUALS
    private LocalDateTime flaggedOn;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
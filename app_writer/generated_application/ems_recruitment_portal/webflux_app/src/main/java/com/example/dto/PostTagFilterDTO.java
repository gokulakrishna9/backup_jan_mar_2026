package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for PostTag search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostTagFilterDTO {
    
    // Filter type: EQUALS
    private Long tagId;
    
    // Filter type: LIKE
    private String tagName;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: EQUALS
    private Integer usageCount;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
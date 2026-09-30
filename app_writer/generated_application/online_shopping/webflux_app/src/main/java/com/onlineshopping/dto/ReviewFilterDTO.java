package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Review search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewFilterDTO {
    
    // Filter type: EQUALS
    private Long userid;
    
    // Filter type: EQUALS
    private Long productid;
    
    // Filter type: EQUALS
    private Integer rating;
    
    // Filter type: EQUALS
    private String title;
    
    // Filter type: EQUALS
    private String comment;
    
    // Filter type: EQUALS
    private LocalDateTime reviewdate;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
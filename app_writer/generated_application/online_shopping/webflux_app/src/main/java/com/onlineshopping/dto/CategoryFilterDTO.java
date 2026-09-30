package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Category search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryFilterDTO {
    
    // Filter type: EQUALS
    private String categoryname;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private String imageurl;
    
    // Filter type: EQUALS
    private Long parentcategoryid;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
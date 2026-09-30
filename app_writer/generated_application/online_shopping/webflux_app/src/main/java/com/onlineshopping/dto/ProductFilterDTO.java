package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Product search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductFilterDTO {
    
    // Filter type: EQUALS
    private String productname;
    
    // Filter type: EQUALS
    private String description;
    
    // Filter type: EQUALS
    private BigDecimal price;
    
    // Filter type: EQUALS
    private Integer stockquantity;
    
    // Filter type: EQUALS
    private String imageurl;
    
    // Filter type: EQUALS
    private String sku;
    
    // Filter type: EQUALS
    private Boolean isactive;
    
    // Filter type: EQUALS
    private Long categoryid;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
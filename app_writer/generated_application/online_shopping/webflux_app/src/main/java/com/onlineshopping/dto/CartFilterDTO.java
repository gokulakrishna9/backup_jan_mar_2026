package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Cart search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CartFilterDTO {
    
    // Filter type: EQUALS
    private Long userid;
    
    // Filter type: EQUALS
    private BigDecimal totalamount;
    
    // Filter type: EQUALS
    private Integer itemcount;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
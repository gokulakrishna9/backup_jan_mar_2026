package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for OrderItem search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderItemFilterDTO {
    
    // Filter type: EQUALS
    private Long orderid;
    
    // Filter type: EQUALS
    private Long productid;
    
    // Filter type: EQUALS
    private Integer quantity;
    
    // Filter type: EQUALS
    private BigDecimal unitprice;
    
    // Filter type: EQUALS
    private BigDecimal subtotal;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
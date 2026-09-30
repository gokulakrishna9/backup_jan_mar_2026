package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Payment search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PaymentFilterDTO {
    
    // Filter type: EQUALS
    private Long orderid;
    
    // Filter type: EQUALS
    private String paymentmethod;
    
    // Filter type: EQUALS
    private BigDecimal amount;
    
    // Filter type: EQUALS
    private LocalDateTime paymentdate;
    
    // Filter type: EQUALS
    private String transactionid;
    
    // Filter type: EQUALS
    private String status;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
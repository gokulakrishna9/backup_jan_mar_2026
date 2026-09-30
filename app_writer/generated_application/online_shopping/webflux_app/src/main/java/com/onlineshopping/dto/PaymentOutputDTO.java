package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Payment responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PaymentOutputDTO {
    
    private Long paymentId;
    
    private Long orderid;
    
    private String paymentmethod;
    
    private BigDecimal amount;
    
    private LocalDateTime paymentdate;
    
    private String transactionid;
    
    private String status;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
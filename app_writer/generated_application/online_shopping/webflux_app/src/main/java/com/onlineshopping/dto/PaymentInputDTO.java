package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for Payment creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PaymentInputDTO {
    
    private Long orderid;
    
    private String paymentmethod;
    
    private BigDecimal amount;
    
    private LocalDateTime paymentdate;
    
    private String transactionid;
    
    private String status;
    
}
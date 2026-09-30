package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for SubscriptionPaymentHistory creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SubscriptionPaymentHistoryInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Amount is required")
    private BigDecimal amount;
    
    @Size(max = 100, message = "Subscriptiontype cannot exceed 100 characters")
    private String subscriptionType;
    
    private String transactionDetails;
    
    @Size(max = 255, message = "Transactionreference cannot exceed 255 characters")
    private String transactionReference;
    
    private LocalDateTime paymentOn;
    
}
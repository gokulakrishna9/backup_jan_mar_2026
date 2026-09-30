package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for SubscriptionPaymentHistory search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SubscriptionPaymentHistoryFilterDTO {
    
    // Filter type: EQUALS
    private Long paymentId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String subscriptionType;
    
    // Filter type: LIKE
    private String transactionDetails;
    
    // Filter type: LIKE
    private String transactionReference;
    
    // Filter type: EQUALS
    private LocalDateTime paymentOn;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
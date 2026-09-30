package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserCoursePurchase search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCoursePurchaseFilterDTO {
    
    // Filter type: EQUALS
    private Long purchaseId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: LIKE
    private String comment;
    
    // Filter type: LIKE
    private String transactionId;
    
    // Filter type: EQUALS
    private LocalDateTime purchasedOn;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
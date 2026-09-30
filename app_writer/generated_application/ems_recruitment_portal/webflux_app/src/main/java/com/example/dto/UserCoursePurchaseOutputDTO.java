package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for UserCoursePurchase responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserCoursePurchaseOutputDTO {
    
    private Long purchaseId;
    
    private Long userId;
    
    private Long courseId;
    
    private String comment;
    
    private BigDecimal amount;
    
    private String transactionId;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime purchasedOn;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
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
 * Input DTO for UserCoursePurchase creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserCoursePurchaseInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    private String comment;
    
    @NotNull(message = "Amount is required")
    private BigDecimal amount;
    
    @Size(max = 255, message = "Transactionid cannot exceed 255 characters")
    private String transactionId;
    
    private LocalDateTime purchasedOn;
    
}
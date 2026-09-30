package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for User search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserFilterDTO {
    
    // Filter type: EQUALS
    private String username;
    
    // Filter type: EQUALS
    private String encryptedpassword;
    
    // Filter type: EQUALS
    private String email;
    
    // Filter type: EQUALS
    private String firstname;
    
    // Filter type: EQUALS
    private String lastname;
    
    // Filter type: EQUALS
    private String phone;
    
    // Filter type: EQUALS
    private String role;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for User responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserOutputDTO {
    
    private Long userId;
    
    private String username;
    
    private String encryptedpassword;
    
    private String email;
    
    private String firstname;
    
    private String lastname;
    
    private String phone;
    
    private String role;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
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
 * Input DTO for User creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInputDTO {
    
    private String username;
    
    private String encryptedpassword;
    
    private String email;
    
    private String firstname;
    
    private String lastname;
    
    private String phone;
    
    private String role;
    
    private Boolean isPublic;  // Optional, defaults to false
}
package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for User search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserFilterDTO {
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String firstName;
    
    // Filter type: LIKE
    private String lastName;
    
    // Filter type: LIKE
    private String gender;
    
    // Filter type: EQUALS
    private LocalDate dateOfBirth;
    
    // Filter type: LIKE
    private String emailAddress;
    
    // Filter type: LIKE
    private String userName;
    
    // Filter type: LIKE
    private String encryptedPassword;
    
    // Filter type: LIKE
    private String phoneNumber;
    
    // Filter type: LIKE
    private String profilePhoto;
    
    // Filter type: EQUALS
    private Boolean isPublic;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
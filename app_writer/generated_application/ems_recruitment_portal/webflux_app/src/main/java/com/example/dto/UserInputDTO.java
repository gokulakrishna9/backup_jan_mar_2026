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
 * Input DTO for User creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInputDTO {
    
    @NotNull(message = "Firstname is required")
    @Size(max = 100, message = "Firstname cannot exceed 100 characters")
    private String firstName;
    
    @NotNull(message = "Lastname is required")
    @Size(max = 100, message = "Lastname cannot exceed 100 characters")
    private String lastName;
    
    private String gender;
    
    private LocalDate dateOfBirth;
    
    @NotNull(message = "Emailaddress is required")
    @Email(message = "Please provide a valid email address")
    @Size(max = 255, message = "Emailaddress cannot exceed 255 characters")
    private String emailAddress;
    
    @NotNull(message = "Username is required")
    @Size(max = 100, message = "Username cannot exceed 100 characters")
    private String userName;
    
    @NotNull(message = "Encryptedpassword is required")
    @Size(max = 255, message = "Encryptedpassword cannot exceed 255 characters")
    private String encryptedPassword;
    
    @Size(max = 30, message = "Phonenumber cannot exceed 30 characters")
    private String phoneNumber;
    
    @Size(max = 255, message = "Profilephoto cannot exceed 255 characters")
    private String profilePhoto;
    
    private Byte isActive;
    
    private Byte isEntity;
    
    @NotNull(message = "Ispublic is required")
    private Boolean isPublic;
    
}
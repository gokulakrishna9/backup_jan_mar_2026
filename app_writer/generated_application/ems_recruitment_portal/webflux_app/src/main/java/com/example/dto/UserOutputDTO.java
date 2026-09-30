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
 * Output DTO for User responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserOutputDTO {
    
    private Long userId;
    
    private String firstName;
    
    private String lastName;
    
    private String gender;
    
    // Format: yyyy-MM-dd
    private LocalDate dateOfBirth;
    
    private String emailAddress;
    
    private String userName;
    
    private String phoneNumber;
    
    private String profilePhoto;
    
    private Byte isActive;
    
    private Byte isEntity;
    
    private Boolean isPublic;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
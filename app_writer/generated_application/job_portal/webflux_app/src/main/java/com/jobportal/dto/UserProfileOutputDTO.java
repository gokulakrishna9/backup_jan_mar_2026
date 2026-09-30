package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for UserProfile responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserProfileOutputDTO {
    
    private Long userProfileId;
    
    private String firstname;
    
    private String lastname;
    
    private String email;
    
    private String phone;
    
    private String bio;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
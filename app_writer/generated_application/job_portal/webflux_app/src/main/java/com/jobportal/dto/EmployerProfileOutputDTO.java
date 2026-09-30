package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for EmployerProfile responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmployerProfileOutputDTO {
    
    private Long employerProfileId;
    
    private String companyname;
    
    private String industry;
    
    private String website;
    
    private String logourl;
    
    private String description;
    
    private String contactemail;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for EmployerProfile creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmployerProfileInputDTO {
    
    private String companyname;
    
    private String industry;
    
    private String website;
    
    private String logourl;
    
    private String description;
    
    private String contactemail;
    
}
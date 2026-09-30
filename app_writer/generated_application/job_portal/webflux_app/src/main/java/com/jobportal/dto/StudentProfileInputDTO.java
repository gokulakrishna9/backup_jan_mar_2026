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
 * Input DTO for StudentProfile creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentProfileInputDTO {
    
    private String resumeurl;
    
    private String skills;
    
    private String educationlevel;
    
    private Boolean isPublic;  // Optional, defaults to false
}
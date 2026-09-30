package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for StudentProfile responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class StudentProfileOutputDTO {
    
    private Long studentProfileId;
    
    private String resumeurl;
    
    private String skills;
    
    private String educationlevel;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
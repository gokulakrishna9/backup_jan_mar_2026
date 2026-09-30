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
 * Input DTO for JobPost creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostInputDTO {
    
    @NotNull(message = "Jobpostsubject is required")
    @Size(max = 255, message = "Jobpostsubject cannot exceed 255 characters")
    private String jobPostSubject;
    
    private String jobPostDescription;
    
    private Long institutionId;
    
    @Size(max = 255, message = "Location cannot exceed 255 characters")
    private String location;
    
    @Size(max = 100, message = "Salaryrange cannot exceed 100 characters")
    private String salaryRange;
    
    private LocalDateTime postedOn;
    
    private LocalDateTime expiresOn;
    
    private Byte isActive;
    
    private Byte isEntity;
    
}
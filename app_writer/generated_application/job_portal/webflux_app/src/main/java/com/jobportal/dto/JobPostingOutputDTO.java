package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for JobPosting responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostingOutputDTO {
    
    private Long jobPostingId;
    
    private String title;
    
    private String description;
    
    private String location;
    
    private BigDecimal salarymin;
    
    private BigDecimal salarymax;
    
    private String jobtype;
    
    private Boolean isactive;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
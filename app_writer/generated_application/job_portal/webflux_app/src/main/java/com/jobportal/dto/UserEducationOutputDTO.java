package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for UserEducation responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEducationOutputDTO {
    
    private Long userEducationId;
    
    private String institutionname;
    
    private String degree;
    
    private String fieldofstudy;
    
    private LocalDate startdate;
    
    private LocalDate enddate;
    
    private String grade;
    
    private String description;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
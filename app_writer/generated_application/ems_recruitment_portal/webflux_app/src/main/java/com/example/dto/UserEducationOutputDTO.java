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
 * Output DTO for UserEducation responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class UserEducationOutputDTO {
    
    private Long educationId;
    
    private Long userId;
    
    private Long institutionId;
    
    private String degreeType;
    
    private String fieldOfStudy;
    
    private String specialization;
    
    // Format: yyyy-MM-dd
    private LocalDate startDate;
    
    // Format: yyyy-MM-dd
    private LocalDate endDate;
    
    private String gradeGpa;
    
    private Byte isVerified;
    
    private Long certificateDocumentId;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
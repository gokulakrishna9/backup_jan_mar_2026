package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Institution responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionOutputDTO {
    
    private Long institutionId;
    
    private String name;
    
    private String country;
    
    private String website;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
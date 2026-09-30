package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CandidateInstituteLink search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CandidateInstituteLinkFilterDTO {
    
    // Filter type: EQUALS
    private Long linkId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String comment;
    
    // Filter type: LIKE
    private String status;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
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
 * Output DTO for CandidateInstituteLink responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CandidateInstituteLinkOutputDTO {
    
    private Long linkId;
    
    private Long userId;
    
    private Long institutionId;
    
    private String comment;
    
    private String status;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
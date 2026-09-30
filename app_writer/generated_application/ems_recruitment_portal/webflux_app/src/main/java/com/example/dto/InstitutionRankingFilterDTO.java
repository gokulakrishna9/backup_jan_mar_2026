package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for InstitutionRanking search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionRankingFilterDTO {
    
    // Filter type: EQUALS
    private Long rankingId;
    
    // Filter type: EQUALS
    private Long institutionId;
    
    // Filter type: LIKE
    private String rankingOrganization;
    
    // Filter type: EQUALS
    private Integer rankingYear;
    
    // Filter type: EQUALS
    private Integer overallRank;
    
    // Filter type: EQUALS
    private Integer countryRank;
    
    // Filter type: LIKE
    private String category;
    
    // Filter type: EQUALS
    private Integer categoryRank;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
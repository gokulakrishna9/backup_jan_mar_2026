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
 * Output DTO for InstitutionRanking responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class InstitutionRankingOutputDTO {
    
    private Long rankingId;
    
    private Long institutionId;
    
    private String rankingOrganization;
    
    private Integer rankingYear;
    
    private Integer overallRank;
    
    private Integer countryRank;
    
    private String category;
    
    private Integer categoryRank;
    
    private BigDecimal score;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
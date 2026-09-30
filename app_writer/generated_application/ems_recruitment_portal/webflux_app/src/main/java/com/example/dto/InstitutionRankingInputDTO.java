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
 * Input DTO for InstitutionRanking creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class InstitutionRankingInputDTO {
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    @NotNull(message = "Rankingorganization is required")
    @Size(max = 255, message = "Rankingorganization cannot exceed 255 characters")
    private String rankingOrganization;
    
    @NotNull(message = "Rankingyear is required")
    private Integer rankingYear;
    
    private Integer overallRank;
    
    private Integer countryRank;
    
    @Size(max = 255, message = "Category cannot exceed 255 characters")
    private String category;
    
    private Integer categoryRank;
    
    private BigDecimal score;
    
}
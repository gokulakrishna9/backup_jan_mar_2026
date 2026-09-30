package com.example.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Entity class for ems_institution_ranking table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution_ranking")
public class InstitutionRanking {
    
    @Id
    @Column("ranking_id")
    private Long rankingId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("ranking_organization")
    private String rankingOrganization;
    
    @Column("ranking_year")
    private Integer rankingYear;
    
    @Column("overall_rank")
    private Integer overallRank;
    
    @Column("country_rank")
    private Integer countryRank;
    
    @Column("category")
    private String category;
    
    @Column("category_rank")
    private Integer categoryRank;
    
    @Column("score")
    private BigDecimal score;
    
}
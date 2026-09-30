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
 * Entity class for ems_ai_institution_profile_evaluation table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_institution_profile_evaluation")
public class AiInstitutionProfileEvaluation {
    
    @Id
    @Column("evaluation_id")
    private Long evaluationId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("evaluation_summary")
    private String evaluationSummary;
    
    @Column("rating")
    private BigDecimal rating;
    
}
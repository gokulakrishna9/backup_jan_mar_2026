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
 * Entity class for ems_ai_community_post_evaluation table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_community_post_evaluation")
public class AiCommunityPostEvaluation {
    
    @Id
    @Column("evaluation_id")
    private Long evaluationId;
    
    @Column("post_id")
    private Long postId;
    
    @Column("evaluation_summary")
    private String evaluationSummary;
    
    @Column("rating")
    private BigDecimal rating;
    
}
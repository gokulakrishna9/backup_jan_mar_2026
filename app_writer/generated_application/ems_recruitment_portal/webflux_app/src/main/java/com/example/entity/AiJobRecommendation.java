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
 * Entity class for ems_ai_job_recommendation table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_job_recommendation")
public class AiJobRecommendation {
    
    @Id
    @Column("preference_id")
    private Long preferenceId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("profile_id")
    private Long profileId;
    
    @Column("preference_rating")
    private BigDecimal preferenceRating;
    
    @Column("recommendation_summary")
    private String recommendationSummary;
    
}
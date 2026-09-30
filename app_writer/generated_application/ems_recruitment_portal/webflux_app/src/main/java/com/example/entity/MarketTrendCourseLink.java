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
 * Entity class for ems_market_trend_course_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_market_trend_course_link")
public class MarketTrendCourseLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("trend_id")
    private Long trendId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("relevance_score")
    private BigDecimal relevanceScore;
    
    @Column("demand_level")
    private String demandLevel;
    
    @Column("recommendation_reason")
    private String recommendationReason;
    
    @Column("ai_generated")
    private Byte aiGenerated;
    
}
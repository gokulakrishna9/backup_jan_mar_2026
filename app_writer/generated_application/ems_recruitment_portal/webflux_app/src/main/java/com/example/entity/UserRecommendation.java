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
 * Entity class for ems_user_recommendation table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_recommendation")
public class UserRecommendation {
    
    @Id
    @Column("recommendation_id")
    private Long recommendationId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("recommended_by_user_id")
    private Long recommendedByUserId;
    
    @Column("recommendation_text")
    private String recommendationText;
    
    @Column("relationship")
    private String relationship;
    
    @Column("position_at_time")
    private String positionAtTime;
    
    @Column("is_visible")
    private Byte isVisible;
    
}
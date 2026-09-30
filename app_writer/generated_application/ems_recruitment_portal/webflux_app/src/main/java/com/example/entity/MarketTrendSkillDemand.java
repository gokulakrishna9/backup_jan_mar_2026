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
 * Entity class for ems_market_trend_skill_demand table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_market_trend_skill_demand")
public class MarketTrendSkillDemand {
    
    @Id
    @Column("demand_id")
    private Long demandId;
    
    @Column("trend_id")
    private Long trendId;
    
    @Column("skill_name")
    private String skillName;
    
    @Column("demand_level")
    private String demandLevel;
    
    @Column("growth_rate")
    private BigDecimal growthRate;
    
    @Column("average_salary_range")
    private String averageSalaryRange;
    
    @Column("job_openings_count")
    private Integer jobOpeningsCount;
    
    @Column("region")
    private String region;
    
    @Column("industry")
    private String industry;
    
}
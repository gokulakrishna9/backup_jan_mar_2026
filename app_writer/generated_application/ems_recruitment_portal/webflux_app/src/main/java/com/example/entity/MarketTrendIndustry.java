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
 * Entity class for ems_market_trend_industry table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_market_trend_industry")
public class MarketTrendIndustry {
    
    @Id
    @Column("industry_id")
    private Long industryId;
    
    @Column("trend_id")
    private Long trendId;
    
    @Column("industry_name")
    private String industryName;
    
    @Column("description")
    private String description;
    
    @Column("growth_rate")
    private BigDecimal growthRate;
    
    @Column("market_size")
    private String marketSize;
    
    @Column("emerging_technologies")
    private String emergingTechnologies;
    
}
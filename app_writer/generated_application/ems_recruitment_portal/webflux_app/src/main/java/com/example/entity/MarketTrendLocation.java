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
 * Entity class for ems_market_trend_location table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_market_trend_location")
public class MarketTrendLocation {
    
    @Id
    @Column("location_id")
    private Long locationId;
    
    @Column("trend_id")
    private Long trendId;
    
    @Column("country")
    private String country;
    
    @Column("region")
    private String region;
    
    @Column("city")
    private String city;
    
    @Column("job_market_health")
    private String jobMarketHealth;
    
    @Column("unemployment_rate")
    private BigDecimal unemploymentRate;
    
    @Column("average_salary")
    private String averageSalary;
    
    @Column("cost_of_living_index")
    private BigDecimal costOfLivingIndex;
    
    @Column("top_industries")
    private String topIndustries;
    
}
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
 * Entity class for ems_ai_market_trend_property table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_market_trend_property")
public class AiMarketTrendProperty {
    
    @Id
    @Column("trend_id")
    private Long trendId;
    
    @Column("trend_name")
    private String trendName;
    
    @Column("trend_description")
    private String trendDescription;
    
}
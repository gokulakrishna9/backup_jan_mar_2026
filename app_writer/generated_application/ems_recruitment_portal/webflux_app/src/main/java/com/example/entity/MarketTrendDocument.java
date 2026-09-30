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
 * Entity class for ems_market_trend_document table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_market_trend_document")
public class MarketTrendDocument {
    
    @Id
    @Column("document_id")
    private Long documentId;
    
    @Column("trend_id")
    private Long trendId;
    
    @Column("title")
    private String title;
    
    @Column("document")
    private String document;
    
    @Column("document_type")
    private String documentType;
    
}
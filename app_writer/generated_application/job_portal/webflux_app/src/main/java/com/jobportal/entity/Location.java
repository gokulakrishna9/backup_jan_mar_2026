package com.jobportal.entity;

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
 * Entity class for location table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "location")
public class Location {
    
    @Id
    @Column("location_id")
    private Long locationId;
    
    @Column("city")
    private String city;
    
    @Column("state")
    private String state;
    
    @Column("country")
    private String country;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
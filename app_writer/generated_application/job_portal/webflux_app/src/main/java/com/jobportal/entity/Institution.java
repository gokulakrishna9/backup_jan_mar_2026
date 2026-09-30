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
 * Entity class for institution table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "institution")
public class Institution {
    
    @Id
    @Column("institution_id")
    private Long institutionId;
    
    @Column("name")
    private String name;
    
    @Column("country")
    private String country;
    
    @Column("website")
    private String website;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
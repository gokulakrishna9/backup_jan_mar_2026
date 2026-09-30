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
 * Entity class for education_level table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "education_level")
public class EducationLevel {
    
    @Id
    @Column("education_level_id")
    private Long educationLevelId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
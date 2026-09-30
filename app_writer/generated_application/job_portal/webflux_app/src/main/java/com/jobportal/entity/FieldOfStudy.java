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
 * Entity class for field_of_study table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "field_of_study")
public class FieldOfStudy {
    
    @Id
    @Column("field_of_study_id")
    private Long fieldOfStudyId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
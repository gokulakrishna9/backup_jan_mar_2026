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
 * Entity class for course_code_lab table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "course_code_lab")
public class CourseCodeLab {
    
    @Id
    @Column("course_code_lab_id")
    private Long courseCodeLabId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("language")
    private String language;
    
    @Column("starter_code")
    private String startercode;
    
    @Column("solution_code")
    private String solutioncode;
    
    @Column("instructions")
    private String instructions;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
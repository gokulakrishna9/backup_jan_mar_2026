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
 * Entity class for user_education table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user_education")
public class UserEducation {
    
    @Id
    @Column("user_education_id")
    private Long userEducationId;
    
    @Column("institution_name")
    private String institutionname;
    
    @Column("degree")
    private String degree;
    
    @Column("field_of_study")
    private String fieldofstudy;
    
    @Column("start_date")
    private LocalDate startdate;
    
    @Column("end_date")
    private LocalDate enddate;
    
    @Column("grade")
    private String grade;
    
    @Column("description")
    private String description;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
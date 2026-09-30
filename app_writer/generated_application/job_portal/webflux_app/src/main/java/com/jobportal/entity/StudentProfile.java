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
 * Entity class for student_profile table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "student_profile")
public class StudentProfile {
    
    @Id
    @Column("student_profile_id")
    private Long studentProfileId;
    
    @Column("resume_url")
    private String resumeurl;
    
    @Column("skills")
    private String skills;
    
    @Column("education_level")
    private String educationlevel;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
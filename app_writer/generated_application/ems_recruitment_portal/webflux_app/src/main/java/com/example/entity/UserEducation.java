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
 * Entity class for ems_user_education table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_education")
public class UserEducation {
    
    @Id
    @Column("education_id")
    private Long educationId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("degree_type")
    private String degreeType;
    
    @Column("field_of_study")
    private String fieldOfStudy;
    
    @Column("specialization")
    private String specialization;
    
    @Column("start_date")
    private LocalDate startDate;
    
    @Column("end_date")
    private LocalDate endDate;
    
    @Column("grade_gpa")
    private String gradeGpa;
    
    @Column("is_verified")
    private Byte isVerified;
    
    @Column("certificate_document_id")
    private Long certificateDocumentId;
    
}
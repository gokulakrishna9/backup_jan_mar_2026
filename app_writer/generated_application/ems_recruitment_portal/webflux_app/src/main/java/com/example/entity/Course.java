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
 * Entity class for ems_course table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course")
public class Course {
    
    @Id
    @Column("course_id")
    private Long courseId;
    
    @Column("course_name")
    private String courseName;
    
    @Column("description")
    private String description;
    
    @Column("outcomes")
    private String outcomes;
    
    @Column("course_type_id")
    private Integer courseTypeId;
    
    @Column("is_published")
    private Byte isPublished;
    
    @Column("price")
    private BigDecimal price;
    
    @Column("duration_weeks")
    private Integer durationWeeks;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("is_entity")
    private Byte isEntity;
    
    @Column("is_public")
    private Boolean isPublic;
    
}
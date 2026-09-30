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
 * Entity class for ems_course_prerequisite table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_prerequisite")
public class CoursePrerequisite {
    
    @Id
    @Column("prerequisite_id")
    private Long prerequisiteId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("prerequisite_course_id")
    private Long prerequisiteCourseId;
    
    @Column("prerequisite_type")
    private String prerequisiteType;
    
    @Column("prerequisite_description")
    private String prerequisiteDescription;
    
    @Column("is_mandatory")
    private Byte isMandatory;
    
}
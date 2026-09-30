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
 * Entity class for ems_course_module table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_module")
public class CourseModule {
    
    @Id
    @Column("module_id")
    private Long moduleId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("module_name")
    private String moduleName;
    
    @Column("module_number")
    private Integer moduleNumber;
    
    @Column("description")
    private String description;
    
    @Column("duration_hours")
    private Integer durationHours;
    
    @Column("learning_objectives")
    private String learningObjectives;
    
    @Column("is_mandatory")
    private Byte isMandatory;
    
    @Column("order_sequence")
    private Integer orderSequence;
    
}
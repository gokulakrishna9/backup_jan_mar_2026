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
 * Entity class for ems_course_assignment table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_assignment")
public class CourseAssignment {
    
    @Id
    @Column("assignment_id")
    private Long assignmentId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("module_id")
    private Long moduleId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("assignment_type")
    private String assignmentType;
    
    @Column("max_score")
    private Integer maxScore;
    
    @Column("passing_score")
    private Integer passingScore;
    
    @Column("due_date")
    private LocalDateTime dueDate;
    
    @Column("duration_minutes")
    private Integer durationMinutes;
    
    @Column("is_mandatory")
    private Byte isMandatory;
    
}
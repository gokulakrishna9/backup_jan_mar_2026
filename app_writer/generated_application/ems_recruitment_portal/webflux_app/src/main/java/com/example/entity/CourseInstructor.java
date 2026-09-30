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
 * Entity class for ems_course_instructor table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_instructor")
public class CourseInstructor {
    
    @Id
    @Column("instructor_link_id")
    private Long instructorLinkId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("role")
    private String role;
    
    @Column("bio")
    private String bio;
    
    @Column("specialization")
    private String specialization;
    
}
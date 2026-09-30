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
 * Entity class for ems_user_course_progress table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_course_progress")
public class UserCourseProgress {
    
    @Id
    @Column("progress_id")
    private Long progressId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("lesson_id")
    private Long lessonId;
    
    @Column("completion_percentage")
    private BigDecimal completionPercentage;
    
    @Column("last_accessed_at")
    private LocalDateTime lastAccessedAt;
    
    @Column("time_spent_minutes")
    private Integer timeSpentMinutes;
    
    @Column("status")
    private String status;
    
}
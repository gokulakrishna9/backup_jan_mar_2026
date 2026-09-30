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
 * Entity class for ems_course_lesson table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_lesson")
public class CourseLesson {
    
    @Id
    @Column("lesson_id")
    private Long lessonId;
    
    @Column("module_id")
    private Long moduleId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("lesson_title")
    private String lessonTitle;
    
    @Column("lesson_number")
    private Integer lessonNumber;
    
    @Column("content_type")
    private String contentType;
    
    @Column("content_url")
    private String contentUrl;
    
    @Column("duration_minutes")
    private Integer durationMinutes;
    
    @Column("is_preview_available")
    private Byte isPreviewAvailable;
    
    @Column("order_sequence")
    private Integer orderSequence;
    
}
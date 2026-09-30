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
 * Entity class for course_question table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "course_question")
public class CourseQuestion {
    
    @Id
    @Column("course_question_id")
    private Long courseQuestionId;
    
    @Column("question_text")
    private String questiontext;
    
    @Column("question_code")
    private String questioncode;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
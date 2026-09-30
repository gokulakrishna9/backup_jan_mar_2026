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
 * Entity class for course_answer table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "course_answer")
public class CourseAnswer {
    
    @Id
    @Column("course_answer_id")
    private Long courseAnswerId;
    
    @Column("answer_text")
    private String answertext;
    
    @Column("answer_code")
    private String answercode;
    
    @Column("is_accepted")
    private Boolean isaccepted;
    
    @Column("upvotes")
    private Integer upvotes;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
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
 * Entity class for exam_answer table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "exam_answer")
public class ExamAnswer {
    
    @Id
    @Column("exam_answer_id")
    private Long examAnswerId;
    
    @Column("answer_text")
    private String answertext;
    
    @Column("answer_code")
    private String answercode;
    
    @Column("is_correct")
    private Boolean iscorrect;
    
    @Column("explanation")
    private String explanation;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
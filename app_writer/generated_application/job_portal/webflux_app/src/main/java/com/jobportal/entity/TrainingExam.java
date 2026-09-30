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
 * Entity class for training_exam table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "training_exam")
public class TrainingExam {
    
    @Id
    @Column("training_exam_id")
    private Long trainingExamId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("passing_score")
    private Integer passingscore;
    
    @Column("max_score")
    private Integer maxscore;
    
    @Column("time_limit_minutes")
    private Integer timelimitminutes;
    
    @Column("max_attempts")
    private Integer maxattempts;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
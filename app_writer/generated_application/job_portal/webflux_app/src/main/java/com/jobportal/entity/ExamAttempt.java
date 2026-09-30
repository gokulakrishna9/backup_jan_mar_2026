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
 * Entity class for exam_attempt table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "exam_attempt")
public class ExamAttempt {
    
    @Id
    @Column("exam_attempt_id")
    private Long examAttemptId;
    
    @Column("score")
    private Integer score;
    
    @Column("passed")
    private Boolean passed;
    
    @Column("started_at")
    private LocalDateTime startedat;
    
    @Column("completed_at")
    private LocalDateTime completedat;
    
    @Column("attempt_number")
    private Integer attemptnumber;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
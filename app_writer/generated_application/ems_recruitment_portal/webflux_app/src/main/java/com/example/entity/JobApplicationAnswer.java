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
 * Entity class for ems_job_application_answer table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_application_answer")
public class JobApplicationAnswer {
    
    @Id
    @Column("answer_id")
    private Long answerId;
    
    @Column("application_id")
    private Long applicationId;
    
    @Column("question_id")
    private Long questionId;
    
    @Column("answer_text")
    private String answerText;
    
    @Column("answer_file_id")
    private Long answerFileId;
    
}
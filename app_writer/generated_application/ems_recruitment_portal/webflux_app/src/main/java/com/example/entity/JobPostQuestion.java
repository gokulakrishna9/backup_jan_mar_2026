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
 * Entity class for ems_job_post_question table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_question")
public class JobPostQuestion {
    
    @Id
    @Column("question_id")
    private Long questionId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("question_text")
    private String questionText;
    
    @Column("question_type")
    private String questionType;
    
    @Column("is_required")
    private Byte isRequired;
    
    @Column("order_sequence")
    private Integer orderSequence;
    
}
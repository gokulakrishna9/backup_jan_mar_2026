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
 * Entity class for ems_user_assignment_submission table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_assignment_submission")
public class UserAssignmentSubmission {
    
    @Id
    @Column("submission_id")
    private Long submissionId;
    
    @Column("assignment_id")
    private Long assignmentId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("submission_content")
    private String submissionContent;
    
    @Column("submission_file_id")
    private Long submissionFileId;
    
    @Column("submitted_at")
    private LocalDateTime submittedAt;
    
    @Column("score")
    private Integer score;
    
    @Column("feedback")
    private String feedback;
    
    @Column("graded_by_user_id")
    private Long gradedByUserId;
    
    @Column("graded_at")
    private LocalDateTime gradedAt;
    
    @Column("status")
    private String status;
    
}
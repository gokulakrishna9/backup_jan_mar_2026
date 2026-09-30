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
 * Entity class for ems_job_application table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_application")
public class JobApplication {
    
    @Id
    @Column("application_id")
    private Long applicationId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("cover_letter")
    private String coverLetter;
    
    @Column("resume_document_id")
    private Long resumeDocumentId;
    
    @Column("application_status")
    private String applicationStatus;
    
    @Column("applied_at")
    private LocalDateTime appliedAt;
    
    @Column("status_updated_at")
    private LocalDateTime statusUpdatedAt;
    
    @Column("status_updated_by_user_id")
    private Long statusUpdatedByUserId;
    
    @Column("notes")
    private String notes;
    
}
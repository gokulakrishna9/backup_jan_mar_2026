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
 * Entity class for job_application table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "job_application")
public class JobApplication {
    
    @Id
    @Column("job_application_id")
    private Long jobApplicationId;
    
    @Column("status")
    private String status;
    
    @Column("cover_letter")
    private String coverletter;
    
    @Column("applied_at")
    private LocalDateTime appliedat;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
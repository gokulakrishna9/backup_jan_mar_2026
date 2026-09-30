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
 * Entity class for ems_job_post table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post")
public class JobPost {
    
    @Id
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("job_post_subject")
    private String jobPostSubject;
    
    @Column("job_post_description")
    private String jobPostDescription;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("location")
    private String location;
    
    @Column("salary_range")
    private String salaryRange;
    
    @Column("posted_on")
    private LocalDateTime postedOn;
    
    @Column("expires_on")
    private LocalDateTime expiresOn;
    
    @Column("is_active")
    private Byte isActive;
    
    @Column("is_entity")
    private Byte isEntity;
    
}
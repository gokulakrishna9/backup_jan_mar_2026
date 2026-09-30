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
 * Entity class for job_posting table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "job_posting")
public class JobPosting {
    
    @Id
    @Column("job_posting_id")
    private Long jobPostingId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("location")
    private String location;
    
    @Column("salary_min")
    private BigDecimal salarymin;
    
    @Column("salary_max")
    private BigDecimal salarymax;
    
    @Column("job_type")
    private String jobtype;
    
    @Column("is_active")
    private Boolean isactive;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
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
 * Entity class for job_title table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "job_title")
public class JobTitle {
    
    @Id
    @Column("job_title_id")
    private Long jobTitleId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
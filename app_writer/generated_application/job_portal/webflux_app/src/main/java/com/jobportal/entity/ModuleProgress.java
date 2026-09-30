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
 * Entity class for module_progress table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "module_progress")
public class ModuleProgress {
    
    @Id
    @Column("module_progress_id")
    private Long moduleProgressId;
    
    @Column("status")
    private String status;
    
    @Column("completed_at")
    private LocalDateTime completedat;
    
    @Column("progress_percent")
    private Integer progresspercent;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
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
 * Entity class for training_module table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "training_module")
public class TrainingModule {
    
    @Id
    @Column("training_module_id")
    private Long trainingModuleId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("module_order")
    private Integer moduleorder;
    
    @Column("duration_minutes")
    private Integer durationminutes;
    
    @Column("content_url")
    private String contenturl;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
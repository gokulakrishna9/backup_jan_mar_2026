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
 * Entity class for training_program table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "training_program")
public class TrainingProgram {
    
    @Id
    @Column("training_program_id")
    private Long trainingProgramId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("duration_days")
    private Integer durationdays;
    
    @Column("price")
    private BigDecimal price;
    
    @Column("is_active")
    private Boolean isactive;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
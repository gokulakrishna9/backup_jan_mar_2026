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
 * Entity class for trainer_profile table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "trainer_profile")
public class TrainerProfile {
    
    @Id
    @Column("trainer_profile_id")
    private Long trainerProfileId;
    
    @Column("specialization")
    private String specialization;
    
    @Column("certifications")
    private String certifications;
    
    @Column("hourly_rate")
    private BigDecimal hourlyrate;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
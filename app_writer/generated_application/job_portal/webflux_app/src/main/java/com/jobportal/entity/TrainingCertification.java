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
 * Entity class for training_certification table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "training_certification")
public class TrainingCertification {
    
    @Id
    @Column("training_certification_id")
    private Long trainingCertificationId;
    
    @Column("certificate_number")
    private String certificatenumber;
    
    @Column("title")
    private String title;
    
    @Column("issued_at")
    private LocalDateTime issuedat;
    
    @Column("expires_at")
    private LocalDateTime expiresat;
    
    @Column("certificate_url")
    private String certificateurl;
    
    @Column("status")
    private String status;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
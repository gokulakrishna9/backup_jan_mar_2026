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
 * Entity class for employer_profile table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "employer_profile")
public class EmployerProfile {
    
    @Id
    @Column("employer_profile_id")
    private Long employerProfileId;
    
    @Column("company_name")
    private String companyname;
    
    @Column("industry")
    private String industry;
    
    @Column("website")
    private String website;
    
    @Column("logo_url")
    private String logourl;
    
    @Column("description")
    private String description;
    
    @Column("contact_email")
    private String contactemail;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
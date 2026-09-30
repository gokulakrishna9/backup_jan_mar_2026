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
 * Entity class for ems_institution_accreditation table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution_accreditation")
public class InstitutionAccreditation {
    
    @Id
    @Column("accreditation_id")
    private Long accreditationId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("accrediting_body")
    private String accreditingBody;
    
    @Column("accreditation_type")
    private String accreditationType;
    
    @Column("accreditation_level")
    private String accreditationLevel;
    
    @Column("issue_date")
    private LocalDate issueDate;
    
    @Column("expiry_date")
    private LocalDate expiryDate;
    
    @Column("certificate_document_id")
    private Long certificateDocumentId;
    
    @Column("is_active")
    private Byte isActive;
    
}
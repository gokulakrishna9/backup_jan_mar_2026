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
 * Entity class for ems_user_certification table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_certification")
public class UserCertification {
    
    @Id
    @Column("certification_id")
    private Long certificationId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("certification_name")
    private String certificationName;
    
    @Column("issuing_organization")
    private String issuingOrganization;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("issue_date")
    private LocalDate issueDate;
    
    @Column("expiry_date")
    private LocalDate expiryDate;
    
    @Column("credential_id")
    private String credentialId;
    
    @Column("credential_url")
    private String credentialUrl;
    
    @Column("certificate_document_id")
    private Long certificateDocumentId;
    
    @Column("is_verified")
    private Byte isVerified;
    
}
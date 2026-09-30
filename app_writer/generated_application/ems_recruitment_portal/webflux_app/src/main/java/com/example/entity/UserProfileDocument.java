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
 * Entity class for ems_user_profile_document table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_profile_document")
public class UserProfileDocument {
    
    @Id
    @Column("document_id")
    private Long documentId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("title")
    private String title;
    
    @Column("document")
    private String document;
    
    @Column("document_type")
    private String documentType;
    
}
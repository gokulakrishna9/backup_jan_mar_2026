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
 * Entity class for ems_institution table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution")
public class Institution {
    
    @Id
    @Column("institution_id")
    private Long institutionId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    @Column("moto")
    private String moto;
    
    @Column("institution_type_id")
    private Integer institutionTypeId;
    
    @Column("website")
    private String website;
    
    @Column("contact_email")
    private String contactEmail;
    
    @Column("contact_phone")
    private String contactPhone;
    
    @Column("is_active")
    private Byte isActive;
    
    @Column("is_entity")
    private Byte isEntity;
    
    @Column("is_public")
    private Boolean isPublic;
    
}
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
 * Entity class for ems_institution_facility table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution_facility")
public class InstitutionFacility {
    
    @Id
    @Column("facility_id")
    private Long facilityId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("facility_name")
    private String facilityName;
    
    @Column("facility_type")
    private String facilityType;
    
    @Column("description")
    private String description;
    
    @Column("capacity")
    private Integer capacity;
    
    @Column("location_id")
    private Long locationId;
    
    @Column("is_available")
    private Byte isAvailable;
    
}
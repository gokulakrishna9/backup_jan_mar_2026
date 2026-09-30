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
 * Entity class for ems_institution_location table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_institution_location")
public class InstitutionLocation {
    
    @Id
    @Column("location_id")
    private Long locationId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("location_type")
    private String locationType;
    
    @Column("address_line1")
    private String addressLine1;
    
    @Column("address_line2")
    private String addressLine2;
    
    @Column("city")
    private String city;
    
    @Column("state_province")
    private String stateProvince;
    
    @Column("country")
    private String country;
    
    @Column("postal_code")
    private String postalCode;
    
    @Column("latitude")
    private BigDecimal latitude;
    
    @Column("longitude")
    private BigDecimal longitude;
    
    @Column("is_primary")
    private Byte isPrimary;
    
}
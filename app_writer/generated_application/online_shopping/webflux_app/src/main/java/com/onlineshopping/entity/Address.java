package com.onlineshopping.entity;

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
 * Entity class for address table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "address")
public class Address {
    
    @Id
    @Column("address_id")
    private Long addressId;
    
    @Column("user_id")
    private Long userid;
    
    @Column("address_line1")
    private String addressline1;
    
    @Column("address_line2")
    private String addressline2;
    
    @Column("city")
    private String city;
    
    @Column("state")
    private String state;
    
    @Column("postal_code")
    private String postalcode;
    
    @Column("country")
    private String country;
    
    @Column("is_default")
    private Boolean isdefault;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
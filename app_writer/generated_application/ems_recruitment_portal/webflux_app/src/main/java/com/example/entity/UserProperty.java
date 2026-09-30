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
 * Entity class for ems_user_property table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_property")
public class UserProperty {
    
    @Id
    @Column("property_id")
    private Long propertyId;
    
    @Column("property_name")
    private String propertyName;
    
    @Column("property_value")
    private String propertyValue;
    
    @Column("property_type")
    private String propertyType;
    
    @Column("property_description")
    private String propertyDescription;
    
    @Column("group_id")
    private Long groupId;
    
    @Column("user_id")
    private Long userId;
    
}
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
 * Entity class for ems_user_institute_property_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_institute_property_link")
public class UserInstitutePropertyLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("property_id")
    private Long propertyId;
    
    @Column("comment")
    private String comment;
    
}
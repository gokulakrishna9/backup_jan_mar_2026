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
 * Entity class for ems_community table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community")
public class Community {
    
    @Id
    @Column("community_id")
    private Long communityId;
    
    @Column("institute_id")
    private Long instituteId;
    
    @Column("name")
    private String name;
    
    @Column("description")
    private String description;
    
    @Column("group_owner_user_id")
    private Long groupOwnerUserId;
    
    @Column("is_entity")
    private Byte isEntity;
    
    @Column("is_public")
    private Boolean isPublic;
    
}
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
 * Entity class for ems_community_category table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community_category")
public class CommunityCategory {
    
    @Id
    @Column("category_id")
    private Long categoryId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("category_name")
    private String categoryName;
    
    @Column("description")
    private String description;
    
    @Column("icon")
    private String icon;
    
    @Column("color")
    private String color;
    
    @Column("order_sequence")
    private Integer orderSequence;
    
}
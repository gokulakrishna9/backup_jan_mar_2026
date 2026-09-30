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
 * Entity class for category table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "category")
public class Category {
    
    @Id
    @Column("category_id")
    private Long categoryId;
    
    @Column("category_name")
    private String categoryname;
    
    @Column("description")
    private String description;
    
    @Column("image_url")
    private String imageurl;
    
    @Column("parent_category_id")
    private Long parentcategoryid;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
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
 * Entity class for product table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "product")
public class Product {
    
    @Id
    @Column("product_id")
    private Long productId;
    
    @Column("product_name")
    private String productname;
    
    @Column("description")
    private String description;
    
    @Column("price")
    private BigDecimal price;
    
    @Column("stock_quantity")
    private Integer stockquantity;
    
    @Column("image_url")
    private String imageurl;
    
    @Column("sku")
    private String sku;
    
    @Column("is_active")
    private Boolean isactive;
    
    @Column("category_id")
    private Long categoryid;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
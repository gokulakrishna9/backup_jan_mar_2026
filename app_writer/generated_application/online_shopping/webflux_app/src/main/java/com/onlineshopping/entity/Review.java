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
 * Entity class for review table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "review")
public class Review {
    
    @Id
    @Column("review_id")
    private Long reviewId;
    
    @Column("user_id")
    private Long userid;
    
    @Column("product_id")
    private Long productid;
    
    @Column("rating")
    private Integer rating;
    
    @Column("title")
    private String title;
    
    @Column("comment")
    private String comment;
    
    @Column("review_date")
    private LocalDateTime reviewdate;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
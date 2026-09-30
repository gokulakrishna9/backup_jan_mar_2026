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
 * Entity class for cart_item table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "cart_item")
public class CartItem {
    
    @Id
    @Column("cart_item_id")
    private Long cartItemId;
    
    @Column("cart_id")
    private Long cartid;
    
    @Column("product_id")
    private Long productid;
    
    @Column("quantity")
    private Integer quantity;
    
    @Column("unit_price")
    private BigDecimal unitprice;
    
    @Column("subtotal")
    private BigDecimal subtotal;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
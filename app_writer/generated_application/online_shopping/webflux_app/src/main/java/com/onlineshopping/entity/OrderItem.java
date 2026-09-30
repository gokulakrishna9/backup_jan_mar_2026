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
 * Entity class for order_item table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "order_item")
public class OrderItem {
    
    @Id
    @Column("order_item_id")
    private Long orderItemId;
    
    @Column("order_id")
    private Long orderid;
    
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
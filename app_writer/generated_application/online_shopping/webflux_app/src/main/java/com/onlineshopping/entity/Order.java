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
 * Entity class for order table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "order")
public class Order {
    
    @Id
    @Column("order_id")
    private Long orderId;
    
    @Column("user_id")
    private Long userid;
    
    @Column("order_date")
    private LocalDateTime orderdate;
    
    @Column("status")
    private String status;
    
    @Column("total_amount")
    private BigDecimal totalamount;
    
    @Column("shipping_address_id")
    private Long shippingaddressid;
    
    @Column("tracking_number")
    private String trackingnumber;
    
    @Column("notes")
    private String notes;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
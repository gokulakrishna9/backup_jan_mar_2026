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
 * Entity class for payment table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "payment")
public class Payment {
    
    @Id
    @Column("payment_id")
    private Long paymentId;
    
    @Column("order_id")
    private Long orderid;
    
    @Column("payment_method")
    private String paymentmethod;
    
    @Column("amount")
    private BigDecimal amount;
    
    @Column("payment_date")
    private LocalDateTime paymentdate;
    
    @Column("transaction_id")
    private String transactionid;
    
    @Column("status")
    private String status;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
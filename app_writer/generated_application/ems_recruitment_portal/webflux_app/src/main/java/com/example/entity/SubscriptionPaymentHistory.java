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
 * Entity class for ems_subscription_payment_history table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_subscription_payment_history")
public class SubscriptionPaymentHistory {
    
    @Id
    @Column("payment_id")
    private Long paymentId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("amount")
    private BigDecimal amount;
    
    @Column("subscription_type")
    private String subscriptionType;
    
    @Column("transaction_details")
    private String transactionDetails;
    
    @Column("transaction_reference")
    private String transactionReference;
    
    @Column("payment_on")
    private LocalDateTime paymentOn;
    
}
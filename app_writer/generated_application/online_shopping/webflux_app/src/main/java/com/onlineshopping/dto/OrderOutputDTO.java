package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Order responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderOutputDTO {
    
    private Long orderId;
    
    private Long userid;
    
    private LocalDateTime orderdate;
    
    private String status;
    
    private BigDecimal totalamount;
    
    private Long shippingaddressid;
    
    private String trackingnumber;
    
    private String notes;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
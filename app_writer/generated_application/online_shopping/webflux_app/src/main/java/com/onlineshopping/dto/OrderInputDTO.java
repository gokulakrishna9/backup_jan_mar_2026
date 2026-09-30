package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for Order creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class OrderInputDTO {
    
    private Long userid;
    
    private LocalDateTime orderdate;
    
    private String status;
    
    private BigDecimal totalamount;
    
    private Long shippingaddressid;
    
    private String trackingnumber;
    
    private String notes;
    
}
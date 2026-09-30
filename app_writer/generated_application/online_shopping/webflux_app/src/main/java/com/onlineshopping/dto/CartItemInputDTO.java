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
 * Input DTO for CartItem creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CartItemInputDTO {
    
    private Long cartid;
    
    private Long productid;
    
    private Integer quantity;
    
    private BigDecimal unitprice;
    
    private BigDecimal subtotal;
    
}
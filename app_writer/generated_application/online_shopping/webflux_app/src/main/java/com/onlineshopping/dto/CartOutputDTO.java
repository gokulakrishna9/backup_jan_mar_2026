package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Cart responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CartOutputDTO {
    
    private Long cartId;
    
    private Long userid;
    
    private BigDecimal totalamount;
    
    private Integer itemcount;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
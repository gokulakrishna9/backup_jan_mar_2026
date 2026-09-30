package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Product responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductOutputDTO {
    
    private Long productId;
    
    private String productname;
    
    private String description;
    
    private BigDecimal price;
    
    private Integer stockquantity;
    
    private String imageurl;
    
    private String sku;
    
    private Boolean isactive;
    
    private Long categoryid;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
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
 * Input DTO for Product creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ProductInputDTO {
    
    private String productname;
    
    private String description;
    
    private BigDecimal price;
    
    private Integer stockquantity;
    
    private String imageurl;
    
    private String sku;
    
    private Boolean isactive;
    
    private Long categoryid;
    
}
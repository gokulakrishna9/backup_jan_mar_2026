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
 * Input DTO for Category creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryInputDTO {
    
    private String categoryname;
    
    private String description;
    
    private String imageurl;
    
    private Long parentcategoryid;
    
}
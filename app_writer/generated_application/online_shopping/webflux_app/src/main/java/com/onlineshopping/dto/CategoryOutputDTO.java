package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Category responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CategoryOutputDTO {
    
    private Long categoryId;
    
    private String categoryname;
    
    private String description;
    
    private String imageurl;
    
    private Long parentcategoryid;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
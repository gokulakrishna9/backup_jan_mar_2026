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
 * Input DTO for Review creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewInputDTO {
    
    private Long userid;
    
    private Long productid;
    
    private Integer rating;
    
    private String title;
    
    private String comment;
    
    private LocalDateTime reviewdate;
    
}
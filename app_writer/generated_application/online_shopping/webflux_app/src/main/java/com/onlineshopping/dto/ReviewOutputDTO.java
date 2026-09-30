package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Review responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class ReviewOutputDTO {
    
    private Long reviewId;
    
    private Long userid;
    
    private Long productid;
    
    private Integer rating;
    
    private String title;
    
    private String comment;
    
    private LocalDateTime reviewdate;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
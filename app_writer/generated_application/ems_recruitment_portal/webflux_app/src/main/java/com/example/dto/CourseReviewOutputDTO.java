package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for CourseReview responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CourseReviewOutputDTO {
    
    private Long reviewId;
    
    private Long courseId;
    
    private Long userId;
    
    private BigDecimal rating;
    
    private String reviewTitle;
    
    private String reviewText;
    
    private Integer helpfulCount;
    
    private Byte isVerifiedPurchase;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
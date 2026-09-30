package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseReview search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseReviewFilterDTO {
    
    // Filter type: EQUALS
    private Long reviewId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String reviewTitle;
    
    // Filter type: LIKE
    private String reviewText;
    
    // Filter type: EQUALS
    private Integer helpfulCount;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for CourseReview creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseReviewInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Rating is required")
    private BigDecimal rating;
    
    @Size(max = 255, message = "Reviewtitle cannot exceed 255 characters")
    private String reviewTitle;
    
    private String reviewText;
    
    private Integer helpfulCount;
    
    private Byte isVerifiedPurchase;
    
}
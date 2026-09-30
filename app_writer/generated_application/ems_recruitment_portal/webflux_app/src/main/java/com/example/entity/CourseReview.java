package com.example.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Entity class for ems_course_review table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_review")
public class CourseReview {
    
    @Id
    @Column("review_id")
    private Long reviewId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("rating")
    private BigDecimal rating;
    
    @Column("review_title")
    private String reviewTitle;
    
    @Column("review_text")
    private String reviewText;
    
    @Column("helpful_count")
    private Integer helpfulCount;
    
    @Column("is_verified_purchase")
    private Byte isVerifiedPurchase;
    
}
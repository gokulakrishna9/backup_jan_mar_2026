package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for PostComment search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostCommentFilterDTO {
    
    // Filter type: EQUALS
    private Long commentId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: LIKE
    private String comment;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
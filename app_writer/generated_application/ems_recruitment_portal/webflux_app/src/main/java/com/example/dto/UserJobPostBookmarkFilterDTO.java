package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserJobPostBookmark search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserJobPostBookmarkFilterDTO {
    
    // Filter type: EQUALS
    private Long bookmarkId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long jobPostId;
    
    // Filter type: LIKE
    private String comment;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
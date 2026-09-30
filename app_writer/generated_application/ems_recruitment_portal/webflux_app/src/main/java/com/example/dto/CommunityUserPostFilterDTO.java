package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityUserPost search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityUserPostFilterDTO {
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String post;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
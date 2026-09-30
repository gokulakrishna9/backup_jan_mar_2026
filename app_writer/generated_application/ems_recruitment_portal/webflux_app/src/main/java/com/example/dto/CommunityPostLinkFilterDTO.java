package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityPostLink search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityPostLinkFilterDTO {
    
    // Filter type: EQUALS
    private Long linkId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
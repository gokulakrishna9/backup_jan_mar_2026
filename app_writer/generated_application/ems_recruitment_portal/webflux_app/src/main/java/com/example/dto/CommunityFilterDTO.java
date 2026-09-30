package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for Community search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityFilterDTO {
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: EQUALS
    private Long instituteId;
    
    // Filter type: LIKE
    private String name;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: EQUALS
    private Long groupOwnerUserId;
    
    // Filter type: EQUALS
    private Boolean isPublic;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
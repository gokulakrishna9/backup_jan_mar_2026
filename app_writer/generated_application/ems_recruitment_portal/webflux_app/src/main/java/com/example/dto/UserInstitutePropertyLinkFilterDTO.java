package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserInstitutePropertyLink search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserInstitutePropertyLinkFilterDTO {
    
    // Filter type: EQUALS
    private Long linkId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: EQUALS
    private Long propertyId;
    
    // Filter type: LIKE
    private String comment;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
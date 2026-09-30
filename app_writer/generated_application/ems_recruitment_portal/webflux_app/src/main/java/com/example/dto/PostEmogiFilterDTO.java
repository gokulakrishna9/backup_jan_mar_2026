package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for PostEmogi search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostEmogiFilterDTO {
    
    // Filter type: EQUALS
    private Long emogiId;
    
    // Filter type: LIKE
    private String name;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String fileLocation;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
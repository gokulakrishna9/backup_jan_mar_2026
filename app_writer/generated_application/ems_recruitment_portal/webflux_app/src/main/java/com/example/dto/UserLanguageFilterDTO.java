package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for UserLanguage search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserLanguageFilterDTO {
    
    // Filter type: EQUALS
    private Long languageId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String languageName;
    
    // Filter type: LIKE
    private String proficiencyLevel;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
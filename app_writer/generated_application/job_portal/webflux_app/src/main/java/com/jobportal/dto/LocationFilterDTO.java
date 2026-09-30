package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Location search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LocationFilterDTO {
    
    // Filter type: EQUALS
    private String city;
    
    // Filter type: EQUALS
    private String state;
    
    // Filter type: EQUALS
    private String country;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
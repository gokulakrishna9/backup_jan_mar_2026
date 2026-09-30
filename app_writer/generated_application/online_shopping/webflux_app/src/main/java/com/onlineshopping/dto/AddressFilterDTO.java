package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Filter DTO for Address search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AddressFilterDTO {
    
    // Filter type: EQUALS
    private Long userid;
    
    // Filter type: EQUALS
    private String addressline1;
    
    // Filter type: EQUALS
    private String addressline2;
    
    // Filter type: EQUALS
    private String city;
    
    // Filter type: EQUALS
    private String state;
    
    // Filter type: EQUALS
    private String postalcode;
    
    // Filter type: EQUALS
    private String country;
    
    // Filter type: EQUALS
    private Boolean isdefault;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
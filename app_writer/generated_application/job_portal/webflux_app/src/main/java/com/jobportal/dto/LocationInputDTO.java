package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for Location creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class LocationInputDTO {
    
    private String city;
    
    private String state;
    
    private String country;
    
}
package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for Address creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AddressInputDTO {
    
    private Long userid;
    
    private String addressline1;
    
    private String addressline2;
    
    private String city;
    
    private String state;
    
    private String postalcode;
    
    private String country;
    
    private Boolean isdefault;
    
}
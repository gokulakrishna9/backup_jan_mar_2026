package com.onlineshopping.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for Address responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class AddressOutputDTO {
    
    private Long addressId;
    
    private Long userid;
    
    private String addressline1;
    
    private String addressline2;
    
    private String city;
    
    private String state;
    
    private String postalcode;
    
    private String country;
    
    private Boolean isdefault;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for CommunityCategory creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityCategoryInputDTO {
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    @NotNull(message = "Categoryname is required")
    @Size(max = 255, message = "Categoryname cannot exceed 255 characters")
    private String categoryName;
    
    private String description;
    
    @Size(max = 100, message = "Icon cannot exceed 100 characters")
    private String icon;
    
    @Size(max = 50, message = "Color cannot exceed 50 characters")
    private String color;
    
    @NotNull(message = "Ordersequence is required")
    private Integer orderSequence;
    
}
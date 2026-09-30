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
 * Input DTO for Community creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityInputDTO {
    
    private Long instituteId;
    
    @NotNull(message = "Name is required")
    @Size(max = 255, message = "Name cannot exceed 255 characters")
    private String name;
    
    private String description;
    
    private Long groupOwnerUserId;
    
    private Byte isEntity;
    
    @NotNull(message = "Ispublic is required")
    private Boolean isPublic;
    
}
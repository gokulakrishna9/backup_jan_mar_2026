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
 * Input DTO for PostTag creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostTagInputDTO {
    
    @NotNull(message = "Tagname is required")
    @Size(max = 100, message = "Tagname cannot exceed 100 characters")
    private String tagName;
    
    private String description;
    
    @Min(value = 0, message = "Usagecount must be positive")
    private Integer usageCount;
    
}
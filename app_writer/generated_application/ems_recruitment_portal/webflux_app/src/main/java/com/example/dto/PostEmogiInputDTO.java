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
 * Input DTO for PostEmogi creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostEmogiInputDTO {
    
    @NotNull(message = "Name is required")
    @Size(max = 150, message = "Name cannot exceed 150 characters")
    private String name;
    
    private String description;
    
    @Size(max = 255, message = "Filelocation cannot exceed 255 characters")
    private String fileLocation;
    
}
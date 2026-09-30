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
 * Input DTO for UserLanguage creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserLanguageInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Languagename is required")
    @Size(max = 100, message = "Languagename cannot exceed 100 characters")
    private String languageName;
    
    private String proficiencyLevel;
    
    private Byte canRead;
    
    private Byte canWrite;
    
    private Byte canSpeak;
    
}
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
 * Input DTO for PostFlag creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostFlagInputDTO {
    
    @NotNull(message = "Type is required")
    @Size(max = 100, message = "Type cannot exceed 100 characters")
    private String type;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    private String reason;
    
    private LocalDateTime flaggedOn;
    
}
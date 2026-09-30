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
 * Input DTO for UserSocialLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSocialLinkInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Platform is required")
    @Size(max = 100, message = "Platform cannot exceed 100 characters")
    private String platform;
    
    @NotNull(message = "Profileurl is required")
    @Size(max = 500, message = "Profileurl cannot exceed 500 characters")
    private String profileUrl;
    
    private Byte isVerified;
    
}
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
 * Input DTO for CommunityUserLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityUserLinkInputDTO {
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @Size(max = 50, message = "Role cannot exceed 50 characters")
    private String role;
    
    private String comment;
    
}
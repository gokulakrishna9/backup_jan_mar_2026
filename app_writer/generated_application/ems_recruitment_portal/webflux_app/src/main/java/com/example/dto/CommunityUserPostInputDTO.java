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
 * Input DTO for CommunityUserPost creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityUserPostInputDTO {
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Post is required")
    private String post;
    
}
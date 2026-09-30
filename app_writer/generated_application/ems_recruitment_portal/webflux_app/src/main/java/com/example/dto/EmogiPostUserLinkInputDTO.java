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
 * Input DTO for EmogiPostUserLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class EmogiPostUserLinkInputDTO {
    
    @NotNull(message = "Emogiid is required")
    private Long emogiId;
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
}
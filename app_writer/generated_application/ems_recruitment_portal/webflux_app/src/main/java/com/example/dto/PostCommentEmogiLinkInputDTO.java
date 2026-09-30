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
 * Input DTO for PostCommentEmogiLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostCommentEmogiLinkInputDTO {
    
    @NotNull(message = "Commentid is required")
    private Long commentId;
    
    @NotNull(message = "Emogiid is required")
    private Long emogiId;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
}
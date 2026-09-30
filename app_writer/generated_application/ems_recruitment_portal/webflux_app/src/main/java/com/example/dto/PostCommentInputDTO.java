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
 * Input DTO for PostComment creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostCommentInputDTO {
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    @NotNull(message = "Comment is required")
    private String comment;
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
}
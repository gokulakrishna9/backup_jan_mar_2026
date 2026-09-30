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
 * Input DTO for PostTagLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostTagLinkInputDTO {
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    @NotNull(message = "Tagid is required")
    private Long tagId;
    
}
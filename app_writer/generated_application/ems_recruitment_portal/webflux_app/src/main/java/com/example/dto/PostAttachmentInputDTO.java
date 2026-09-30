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
 * Input DTO for PostAttachment creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostAttachmentInputDTO {
    
    @NotNull(message = "Postid is required")
    private Long postId;
    
    @NotNull(message = "Filename is required")
    @Size(max = 255, message = "Filename cannot exceed 255 characters")
    private String fileName;
    
    @Size(max = 100, message = "Filetype cannot exceed 100 characters")
    private String fileType;
    
    @NotNull(message = "Fileurl is required")
    @Size(max = 500, message = "Fileurl cannot exceed 500 characters")
    private String fileUrl;
    
    private Integer fileSizeKb;
    
    @Size(max = 500, message = "Thumbnailurl cannot exceed 500 characters")
    private String thumbnailUrl;
    
}
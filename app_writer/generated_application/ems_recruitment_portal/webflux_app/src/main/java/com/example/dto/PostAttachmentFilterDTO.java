package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for PostAttachment search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PostAttachmentFilterDTO {
    
    // Filter type: EQUALS
    private Long attachmentId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: LIKE
    private String fileName;
    
    // Filter type: LIKE
    private String fileType;
    
    // Filter type: LIKE
    private String fileUrl;
    
    // Filter type: EQUALS
    private Integer fileSizeKb;
    
    // Filter type: LIKE
    private String thumbnailUrl;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
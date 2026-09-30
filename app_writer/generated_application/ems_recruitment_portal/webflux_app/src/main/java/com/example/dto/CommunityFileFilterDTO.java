package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityFile search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityFileFilterDTO {
    
    // Filter type: EQUALS
    private Long fileId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: EQUALS
    private Long postId;
    
    // Filter type: EQUALS
    private Long eventId;
    
    // Filter type: LIKE
    private String fileName;
    
    // Filter type: LIKE
    private String originalFileName;
    
    // Filter type: LIKE
    private String fileType;
    
    // Filter type: LIKE
    private String fileExtension;
    
    // Filter type: LIKE
    private String fileLocation;
    
    // Filter type: EQUALS
    private Long fileSizeBytes;
    
    // Filter type: LIKE
    private String mimeType;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String comment;
    
    // Filter type: LIKE
    private String category;
    
    // Filter type: EQUALS
    private Long uploadedByUserId;
    
    // Filter type: EQUALS
    private Integer downloadCount;
    
    // Filter type: LIKE
    private String thumbnailLocation;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
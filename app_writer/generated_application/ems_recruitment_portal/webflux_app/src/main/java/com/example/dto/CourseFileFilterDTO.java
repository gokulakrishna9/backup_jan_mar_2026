package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CourseFile search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseFileFilterDTO {
    
    // Filter type: EQUALS
    private Long fileId;
    
    // Filter type: EQUALS
    private Long courseId;
    
    // Filter type: EQUALS
    private Long moduleId;
    
    // Filter type: EQUALS
    private Long lessonId;
    
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
    private Integer downloadCount;
    
    // Filter type: LIKE
    private String thumbnailLocation;
    
    // Filter type: EQUALS
    private Integer durationSeconds;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
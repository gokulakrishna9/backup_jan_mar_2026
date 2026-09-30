package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for MarketTrendFile responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class MarketTrendFileOutputDTO {
    
    private Long fileId;
    
    private Long trendId;
    
    private String fileName;
    
    private String originalFileName;
    
    private String fileType;
    
    private String fileExtension;
    
    private String fileLocation;
    
    private Long fileSizeBytes;
    
    private String mimeType;
    
    private String description;
    
    private String comment;
    
    private String category;
    
    private String source;
    
    // Format: yyyy-MM-dd
    private LocalDate reportDate;
    
    private Integer downloadCount;
    
    private String thumbnailLocation;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
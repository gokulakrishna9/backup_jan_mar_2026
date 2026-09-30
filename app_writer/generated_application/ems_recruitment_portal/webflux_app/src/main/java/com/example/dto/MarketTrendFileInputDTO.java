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
 * Input DTO for MarketTrendFile creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class MarketTrendFileInputDTO {
    
    @NotNull(message = "Trendid is required")
    private Long trendId;
    
    @NotNull(message = "Filename is required")
    @Size(max = 255, message = "Filename cannot exceed 255 characters")
    private String fileName;
    
    @NotNull(message = "Originalfilename is required")
    @Size(max = 255, message = "Originalfilename cannot exceed 255 characters")
    private String originalFileName;
    
    @NotNull(message = "Filetype is required")
    private String fileType;
    
    @Size(max = 20, message = "Fileextension cannot exceed 20 characters")
    private String fileExtension;
    
    @NotNull(message = "Filelocation is required")
    @Size(max = 500, message = "Filelocation cannot exceed 500 characters")
    private String fileLocation;
    
    private Long fileSizeBytes;
    
    @Size(max = 100, message = "Mimetype cannot exceed 100 characters")
    private String mimeType;
    
    private String description;
    
    private String comment;
    
    @Size(max = 100, message = "Category cannot exceed 100 characters")
    private String category;
    
    @Size(max = 255, message = "Source cannot exceed 255 characters")
    private String source;
    
    private LocalDate reportDate;
    
    private Integer downloadCount;
    
    @Size(max = 500, message = "Thumbnaillocation cannot exceed 500 characters")
    private String thumbnailLocation;
    
}
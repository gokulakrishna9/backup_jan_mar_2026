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
 * Input DTO for Course creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseInputDTO {
    
    @NotNull(message = "Coursename is required")
    @Size(max = 255, message = "Coursename cannot exceed 255 characters")
    private String courseName;
    
    private String description;
    
    private String outcomes;
    
    private Integer courseTypeId;
    
    private Byte isPublished;
    
    private BigDecimal price;
    
    private Integer durationWeeks;
    
    private Long institutionId;
    
    private Byte isEntity;
    
    @NotNull(message = "Ispublic is required")
    private Boolean isPublic;
    
}
package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for CourseVideo responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseVideoOutputDTO {
    
    private Long courseVideoId;
    
    private String title;
    
    private String description;
    
    private String videourl;
    
    private Integer durationseconds;
    
    private Integer sortorder;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
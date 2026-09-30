package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Output DTO for CourseAudio responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseAudioOutputDTO {
    
    private Long courseAudioId;
    
    private String title;
    
    private String description;
    
    private String audiourl;
    
    private Integer durationseconds;
    
    private Integer sortorder;
    
    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
}
package com.jobportal.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import jakarta.validation.constraints.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;

/**
 * Input DTO for CourseVideo creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseVideoInputDTO {
    
    private String title;
    
    private String description;
    
    private String videourl;
    
    private Integer durationseconds;
    
    private Integer sortorder;
    
}
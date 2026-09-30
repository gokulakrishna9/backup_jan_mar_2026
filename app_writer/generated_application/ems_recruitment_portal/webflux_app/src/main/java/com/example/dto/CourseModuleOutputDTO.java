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
 * Output DTO for CourseModule responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class CourseModuleOutputDTO {
    
    private Long moduleId;
    
    private Long courseId;
    
    private String moduleName;
    
    private Integer moduleNumber;
    
    private String description;
    
    private Integer durationHours;
    
    private String learningObjectives;
    
    private Byte isMandatory;
    
    private Integer orderSequence;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
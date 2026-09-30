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
 * Input DTO for UserEducation creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserEducationInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    private Long institutionId;
    
    @NotNull(message = "Degreetype is required")
    @Size(max = 100, message = "Degreetype cannot exceed 100 characters")
    private String degreeType;
    
    @NotNull(message = "Fieldofstudy is required")
    @Size(max = 255, message = "Fieldofstudy cannot exceed 255 characters")
    private String fieldOfStudy;
    
    @Size(max = 255, message = "Specialization cannot exceed 255 characters")
    private String specialization;
    
    @NotNull(message = "Startdate is required")
    private LocalDate startDate;
    
    private LocalDate endDate;
    
    @Size(max = 50, message = "Gradegpa cannot exceed 50 characters")
    private String gradeGpa;
    
    private Byte isVerified;
    
    private Long certificateDocumentId;
    
}
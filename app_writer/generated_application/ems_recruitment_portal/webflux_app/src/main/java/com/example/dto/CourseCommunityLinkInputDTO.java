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
 * Input DTO for CourseCommunityLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CourseCommunityLinkInputDTO {
    
    @NotNull(message = "Courseid is required")
    private Long courseId;
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    private String linkType;
    
    private Byte isActive;
    
}
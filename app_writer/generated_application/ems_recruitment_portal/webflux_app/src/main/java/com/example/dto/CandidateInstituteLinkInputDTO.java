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
 * Input DTO for CandidateInstituteLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CandidateInstituteLinkInputDTO {
    
    @NotNull(message = "Userid is required")
    private Long userId;
    
    @NotNull(message = "Institutionid is required")
    private Long institutionId;
    
    private String comment;
    
    @Size(max = 50, message = "Status cannot exceed 50 characters")
    private String status;
    
}
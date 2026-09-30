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
 * Input DTO for UserSkillEndorsement creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserSkillEndorsementInputDTO {
    
    @NotNull(message = "Skillid is required")
    private Long skillId;
    
    @NotNull(message = "Endorsedbyuserid is required")
    private Long endorsedByUserId;
    
    private String endorsementComment;
    
    @Size(max = 100, message = "Relationship cannot exceed 100 characters")
    private String relationship;
    
}
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
 * Input DTO for CommunityRule creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityRuleInputDTO {
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    @NotNull(message = "Ruletitle is required")
    @Size(max = 255, message = "Ruletitle cannot exceed 255 characters")
    private String ruleTitle;
    
    @NotNull(message = "Ruledescription is required")
    private String ruleDescription;
    
    @NotNull(message = "Ordersequence is required")
    private Integer orderSequence;
    
}
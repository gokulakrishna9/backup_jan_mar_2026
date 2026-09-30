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
 * Input DTO for JobPostCommunityLink creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class JobPostCommunityLinkInputDTO {
    
    @NotNull(message = "Jobpostid is required")
    private Long jobPostId;
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    private Byte isFeatured;
    
    private Long postedByUserId;
    
}
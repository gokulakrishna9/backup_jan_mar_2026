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
 * Output DTO for JobPost responses.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@JsonInclude(JsonInclude.Include.NON_NULL)
public class JobPostOutputDTO {
    
    private Long jobPostId;
    
    private String jobPostSubject;
    
    private String jobPostDescription;
    
    private Long institutionId;
    
    private String location;
    
    private String salaryRange;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime postedOn;
    
    // Format: yyyy-MM-dd'T'HH:mm:ss
    private LocalDateTime expiresOn;
    
    private Byte isActive;
    
    private Byte isEntity;
    
    private Long createdById;
    private Long updatedById;
    private LocalDateTime createdOn;
    private LocalDateTime updatedOn;
    // Related entities can be included here
}
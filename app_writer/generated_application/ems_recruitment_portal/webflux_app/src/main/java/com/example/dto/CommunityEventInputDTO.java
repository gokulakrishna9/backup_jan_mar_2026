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
 * Input DTO for CommunityEvent creation and updates.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityEventInputDTO {
    
    @NotNull(message = "Communityid is required")
    private Long communityId;
    
    @NotNull(message = "Eventtitle is required")
    @Size(max = 255, message = "Eventtitle cannot exceed 255 characters")
    private String eventTitle;
    
    private String description;
    
    private String eventType;
    
    @NotNull(message = "Startdatetime is required")
    private LocalDateTime startDatetime;
    
    @NotNull(message = "Enddatetime is required")
    private LocalDateTime endDatetime;
    
    @Size(max = 255, message = "Location cannot exceed 255 characters")
    private String location;
    
    @Size(max = 500, message = "Meetinglink cannot exceed 500 characters")
    private String meetingLink;
    
    private Integer maxAttendees;
    
    @NotNull(message = "Organizeruserid is required")
    private Long organizerUserId;
    
}
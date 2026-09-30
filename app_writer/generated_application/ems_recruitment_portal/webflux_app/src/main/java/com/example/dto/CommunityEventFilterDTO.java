package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityEvent search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityEventFilterDTO {
    
    // Filter type: EQUALS
    private Long eventId;
    
    // Filter type: EQUALS
    private Long communityId;
    
    // Filter type: LIKE
    private String eventTitle;
    
    // Filter type: LIKE
    private String description;
    
    // Filter type: LIKE
    private String eventType;
    
    // Filter type: EQUALS
    private LocalDateTime startDatetime;
    
    // Filter type: EQUALS
    private LocalDateTime endDatetime;
    
    // Filter type: LIKE
    private String location;
    
    // Filter type: LIKE
    private String meetingLink;
    
    // Filter type: EQUALS
    private Integer maxAttendees;
    
    // Filter type: EQUALS
    private Long organizerUserId;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
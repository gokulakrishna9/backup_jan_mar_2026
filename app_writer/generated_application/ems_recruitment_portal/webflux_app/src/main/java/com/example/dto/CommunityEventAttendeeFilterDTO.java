package com.example.dto;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import java.time.LocalDateTime;
import java.time.LocalDate;

/**
 * Filter DTO for CommunityEventAttendee search and filtering.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CommunityEventAttendeeFilterDTO {
    
    // Filter type: EQUALS
    private Long attendeeId;
    
    // Filter type: EQUALS
    private Long eventId;
    
    // Filter type: EQUALS
    private Long userId;
    
    // Filter type: LIKE
    private String rsvpStatus;
    
    // Date range filters
    private LocalDateTime createdAfter;
    private LocalDateTime createdBefore;
    private LocalDateTime updatedAfter;
    private LocalDateTime updatedBefore;
}
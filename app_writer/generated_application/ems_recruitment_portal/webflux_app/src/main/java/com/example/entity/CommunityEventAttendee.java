package com.example.entity;

import lombok.Data;
import lombok.Builder;
import lombok.NoArgsConstructor;
import lombok.AllArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import org.springframework.data.relational.core.mapping.Column;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.UUID;

/**
 * Entity class for ems_community_event_attendee table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community_event_attendee")
public class CommunityEventAttendee {
    
    @Id
    @Column("attendee_id")
    private Long attendeeId;
    
    @Column("event_id")
    private Long eventId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("rsvp_status")
    private String rsvpStatus;
    
    @Column("attended")
    private Byte attended;
    
}
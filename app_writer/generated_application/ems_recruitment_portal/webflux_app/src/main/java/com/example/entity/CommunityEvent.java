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
 * Entity class for ems_community_event table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community_event")
public class CommunityEvent {
    
    @Id
    @Column("event_id")
    private Long eventId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("event_title")
    private String eventTitle;
    
    @Column("description")
    private String description;
    
    @Column("event_type")
    private String eventType;
    
    @Column("start_datetime")
    private LocalDateTime startDatetime;
    
    @Column("end_datetime")
    private LocalDateTime endDatetime;
    
    @Column("location")
    private String location;
    
    @Column("meeting_link")
    private String meetingLink;
    
    @Column("max_attendees")
    private Integer maxAttendees;
    
    @Column("organizer_user_id")
    private Long organizerUserId;
    
}
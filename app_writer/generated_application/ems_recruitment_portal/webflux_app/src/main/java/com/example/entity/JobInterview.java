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
 * Entity class for ems_job_interview table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_interview")
public class JobInterview {
    
    @Id
    @Column("interview_id")
    private Long interviewId;
    
    @Column("application_id")
    private Long applicationId;
    
    @Column("interview_type")
    private String interviewType;
    
    @Column("interview_round")
    private Integer interviewRound;
    
    @Column("scheduled_at")
    private LocalDateTime scheduledAt;
    
    @Column("duration_minutes")
    private Integer durationMinutes;
    
    @Column("location")
    private String location;
    
    @Column("meeting_link")
    private String meetingLink;
    
    @Column("interviewer_user_id")
    private Long interviewerUserId;
    
    @Column("status")
    private String status;
    
    @Column("feedback")
    private String feedback;
    
    @Column("rating")
    private BigDecimal rating;
    
}
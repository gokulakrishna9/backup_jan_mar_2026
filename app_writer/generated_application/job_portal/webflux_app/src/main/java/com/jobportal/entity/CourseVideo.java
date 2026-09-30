package com.jobportal.entity;

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
 * Entity class for course_video table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "course_video")
public class CourseVideo {
    
    @Id
    @Column("course_video_id")
    private Long courseVideoId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("video_url")
    private String videourl;
    
    @Column("duration_seconds")
    private Integer durationseconds;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
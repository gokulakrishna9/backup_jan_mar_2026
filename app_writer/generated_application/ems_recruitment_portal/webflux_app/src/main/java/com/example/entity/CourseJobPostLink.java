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
 * Entity class for ems_course_job_post_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_job_post_link")
public class CourseJobPostLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("relevance_score")
    private BigDecimal relevanceScore;
    
    @Column("matching_skills")
    private String matchingSkills;
    
    @Column("ai_generated")
    private Byte aiGenerated;
    
}
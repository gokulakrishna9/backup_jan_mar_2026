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
 * Entity class for ems_user_job_post_bookmark table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_job_post_bookmark")
public class UserJobPostBookmark {
    
    @Id
    @Column("bookmark_id")
    private Long bookmarkId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("comment")
    private String comment;
    
}
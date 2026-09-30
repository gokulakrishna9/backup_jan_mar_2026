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
 * Entity class for ems_job_post_user_bookmark table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_user_bookmark")
public class JobPostUserBookmark {
    
    @Id
    @Column("bookmark_id")
    private Long bookmarkId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("comment")
    private String comment;
    
}
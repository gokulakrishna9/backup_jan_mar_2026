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
 * Entity class for ems_job_post_community_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_community_link")
public class JobPostCommunityLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("is_featured")
    private Byte isFeatured;
    
    @Column("posted_by_user_id")
    private Long postedByUserId;
    
}
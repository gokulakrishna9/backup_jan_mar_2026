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
 * Entity class for ems_community_user_post table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community_user_post")
public class CommunityUserPost {
    
    @Id
    @Column("post_id")
    private Long postId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("post")
    private String post;
    
}
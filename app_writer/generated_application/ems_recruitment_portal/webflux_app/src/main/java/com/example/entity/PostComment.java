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
 * Entity class for ems_post_comment table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_comment")
public class PostComment {
    
    @Id
    @Column("comment_id")
    private Long commentId;
    
    @Column("post_id")
    private Long postId;
    
    @Column("comment")
    private String comment;
    
    @Column("user_id")
    private Long userId;
    
}
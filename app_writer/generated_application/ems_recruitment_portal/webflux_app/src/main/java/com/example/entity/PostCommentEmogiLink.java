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
 * Entity class for ems_post_comment_emogi_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_comment_emogi_link")
public class PostCommentEmogiLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("comment_id")
    private Long commentId;
    
    @Column("emogi_id")
    private Long emogiId;
    
    @Column("user_id")
    private Long userId;
    
}
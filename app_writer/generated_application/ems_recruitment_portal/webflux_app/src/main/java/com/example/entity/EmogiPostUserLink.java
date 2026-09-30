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
 * Entity class for ems_emogi_post_user_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_emogi_post_user_link")
public class EmogiPostUserLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("emogi_id")
    private Long emogiId;
    
    @Column("post_id")
    private Long postId;
    
    @Column("user_id")
    private Long userId;
    
}
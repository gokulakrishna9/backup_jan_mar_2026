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
 * Entity class for ems_post_flag table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_flag")
public class PostFlag {
    
    @Id
    @Column("flag_id")
    private Long flagId;
    
    @Column("type")
    private String type;
    
    @Column("user_id")
    private Long userId;
    
    @Column("post_id")
    private Long postId;
    
    @Column("reason")
    private String reason;
    
    @Column("flagged_on")
    private LocalDateTime flaggedOn;
    
}
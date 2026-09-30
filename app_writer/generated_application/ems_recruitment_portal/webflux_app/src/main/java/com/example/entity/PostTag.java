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
 * Entity class for ems_post_tag table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_tag")
public class PostTag {
    
    @Id
    @Column("tag_id")
    private Long tagId;
    
    @Column("tag_name")
    private String tagName;
    
    @Column("description")
    private String description;
    
    @Column("usage_count")
    private Integer usageCount;
    
}
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
 * Entity class for ems_post_attachment table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_post_attachment")
public class PostAttachment {
    
    @Id
    @Column("attachment_id")
    private Long attachmentId;
    
    @Column("post_id")
    private Long postId;
    
    @Column("file_name")
    private String fileName;
    
    @Column("file_type")
    private String fileType;
    
    @Column("file_url")
    private String fileUrl;
    
    @Column("file_size_kb")
    private Integer fileSizeKb;
    
    @Column("thumbnail_url")
    private String thumbnailUrl;
    
}
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
 * Entity class for ems_job_post_file table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_file")
public class JobPostFile {
    
    @Id
    @Column("file_id")
    private Long fileId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("application_id")
    private Long applicationId;
    
    @Column("file_name")
    private String fileName;
    
    @Column("original_file_name")
    private String originalFileName;
    
    @Column("file_type")
    private String fileType;
    
    @Column("file_extension")
    private String fileExtension;
    
    @Column("file_location")
    private String fileLocation;
    
    @Column("file_size_bytes")
    private Long fileSizeBytes;
    
    @Column("mime_type")
    private String mimeType;
    
    @Column("description")
    private String description;
    
    @Column("comment")
    private String comment;
    
    @Column("category")
    private String category;
    
    @Column("uploaded_by_user_id")
    private Long uploadedByUserId;
    
    @Column("download_count")
    private Integer downloadCount;
    
    @Column("thumbnail_location")
    private String thumbnailLocation;
    
}
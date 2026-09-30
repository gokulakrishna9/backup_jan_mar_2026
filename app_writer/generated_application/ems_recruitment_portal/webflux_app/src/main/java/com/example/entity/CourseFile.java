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
 * Entity class for ems_course_file table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_file")
public class CourseFile {
    
    @Id
    @Column("file_id")
    private Long fileId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("module_id")
    private Long moduleId;
    
    @Column("lesson_id")
    private Long lessonId;
    
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
    
    @Column("is_downloadable")
    private Byte isDownloadable;
    
    @Column("requires_enrollment")
    private Byte requiresEnrollment;
    
    @Column("download_count")
    private Integer downloadCount;
    
    @Column("thumbnail_location")
    private String thumbnailLocation;
    
    @Column("duration_seconds")
    private Integer durationSeconds;
    
}
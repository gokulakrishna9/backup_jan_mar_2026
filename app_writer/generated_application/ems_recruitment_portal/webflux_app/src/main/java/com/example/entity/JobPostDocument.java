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
 * Entity class for ems_job_post_document table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_document")
public class JobPostDocument {
    
    @Id
    @Column("document_id")
    private Long documentId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("title")
    private String title;
    
    @Column("document")
    private String document;
    
    @Column("document_type")
    private String documentType;
    
    @Column("file_name")
    private String fileName;
    
}
package com.jobportal.entity;

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
 * Entity class for course_document table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "course_document")
public class CourseDocument {
    
    @Id
    @Column("course_document_id")
    private Long courseDocumentId;
    
    @Column("title")
    private String title;
    
    @Column("content")
    private String content;
    
    @Column("sort_order")
    private Integer sortorder;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
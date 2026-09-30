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
 * Entity class for ems_course_document table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_document")
public class CourseDocument {
    
    @Id
    @Column("document_id")
    private Long documentId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("group_id")
    private Long groupId;
    
    @Column("title")
    private String title;
    
    @Column("document")
    private String document;
    
    @Column("document_type")
    private String documentType;
    
    @Column("file_name")
    private String fileName;
    
}
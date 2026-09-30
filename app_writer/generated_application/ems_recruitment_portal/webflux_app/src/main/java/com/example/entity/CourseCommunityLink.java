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
 * Entity class for ems_course_community_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_course_community_link")
public class CourseCommunityLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("course_id")
    private Long courseId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("link_type")
    private String linkType;
    
    @Column("is_active")
    private Byte isActive;
    
}
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
 * Entity class for ems_job_post_requirement table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_requirement")
public class JobPostRequirement {
    
    @Id
    @Column("requirement_id")
    private Long requirementId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("requirement_type")
    private String requirementType;
    
    @Column("requirement_description")
    private String requirementDescription;
    
    @Column("is_mandatory")
    private Byte isMandatory;
    
    @Column("minimum_years")
    private Integer minimumYears;
    
    @Column("proficiency_level")
    private String proficiencyLevel;
    
}
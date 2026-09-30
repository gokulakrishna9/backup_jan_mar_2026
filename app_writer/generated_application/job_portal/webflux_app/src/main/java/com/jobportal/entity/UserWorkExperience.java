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
 * Entity class for user_work_experience table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user_work_experience")
public class UserWorkExperience {
    
    @Id
    @Column("user_work_experience_id")
    private Long userWorkExperienceId;
    
    @Column("company_name")
    private String companyname;
    
    @Column("job_title")
    private String jobtitle;
    
    @Column("industry")
    private String industry;
    
    @Column("location")
    private String location;
    
    @Column("start_date")
    private LocalDate startdate;
    
    @Column("end_date")
    private LocalDate enddate;
    
    @Column("is_current")
    private Boolean iscurrent;
    
    @Column("description")
    private String description;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
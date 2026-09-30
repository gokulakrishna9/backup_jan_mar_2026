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
 * Entity class for ems_user_work_experience table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_work_experience")
public class UserWorkExperience {
    
    @Id
    @Column("experience_id")
    private Long experienceId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("job_title")
    private String jobTitle;
    
    @Column("company_name")
    private String companyName;
    
    @Column("employment_type")
    private String employmentType;
    
    @Column("location")
    private String location;
    
    @Column("start_date")
    private LocalDate startDate;
    
    @Column("end_date")
    private LocalDate endDate;
    
    @Column("is_current")
    private Byte isCurrent;
    
    @Column("responsibilities")
    private String responsibilities;
    
    @Column("achievements")
    private String achievements;
    
    @Column("skills_used")
    private String skillsUsed;
    
}
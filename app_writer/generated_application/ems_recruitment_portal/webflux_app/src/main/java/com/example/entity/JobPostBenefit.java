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
 * Entity class for ems_job_post_benefit table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_job_post_benefit")
public class JobPostBenefit {
    
    @Id
    @Column("benefit_id")
    private Long benefitId;
    
    @Column("job_post_id")
    private Long jobPostId;
    
    @Column("benefit_type")
    private String benefitType;
    
    @Column("benefit_description")
    private String benefitDescription;
    
}
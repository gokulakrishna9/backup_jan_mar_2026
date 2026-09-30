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
 * Entity class for user_skill table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user_skill")
public class UserSkill {
    
    @Id
    @Column("user_skill_id")
    private Long userSkillId;
    
    @Column("skill_name")
    private String skillname;
    
    @Column("proficiency_level")
    private String proficiencylevel;
    
    @Column("years_of_experience")
    private Integer yearsofexperience;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
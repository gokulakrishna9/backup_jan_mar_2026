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
 * Entity class for ems_user_skill table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_skill")
public class UserSkill {
    
    @Id
    @Column("skill_id")
    private Long skillId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("skill_name")
    private String skillName;
    
    @Column("skill_category")
    private String skillCategory;
    
    @Column("proficiency_level")
    private String proficiencyLevel;
    
    @Column("years_of_experience")
    private Integer yearsOfExperience;
    
    @Column("is_verified")
    private Byte isVerified;
    
    @Column("verified_by_institution_id")
    private Long verifiedByInstitutionId;
    
    @Column("endorsement_count")
    private Integer endorsementCount;
    
}
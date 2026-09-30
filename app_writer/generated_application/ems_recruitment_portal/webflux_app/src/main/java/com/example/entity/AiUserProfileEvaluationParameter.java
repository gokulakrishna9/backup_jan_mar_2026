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
 * Entity class for ems_ai_user_profile_evaluation_parameter table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_user_profile_evaluation_parameter")
public class AiUserProfileEvaluationParameter {
    
    @Id
    @Column("parameter_id")
    private Long parameterId;
    
    @Column("parameter_name")
    private String parameterName;
    
    @Column("group_id")
    private Long groupId;
    
    @Column("parameter_value")
    private String parameterValue;
    
}
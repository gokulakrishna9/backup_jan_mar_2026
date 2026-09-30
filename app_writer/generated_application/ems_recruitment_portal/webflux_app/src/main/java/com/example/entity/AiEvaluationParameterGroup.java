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
 * Entity class for ems_ai_evaluation_parameter_group table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_ai_evaluation_parameter_group")
public class AiEvaluationParameterGroup {
    
    @Id
    @Column("group_id")
    private Long groupId;
    
    @Column("group_name")
    private String groupName;
    
    @Column("description")
    private String description;
    
}
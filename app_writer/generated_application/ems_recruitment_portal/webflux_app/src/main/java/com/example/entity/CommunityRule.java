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
 * Entity class for ems_community_rule table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_community_rule")
public class CommunityRule {
    
    @Id
    @Column("rule_id")
    private Long ruleId;
    
    @Column("community_id")
    private Long communityId;
    
    @Column("rule_title")
    private String ruleTitle;
    
    @Column("rule_description")
    private String ruleDescription;
    
    @Column("order_sequence")
    private Integer orderSequence;
    
}
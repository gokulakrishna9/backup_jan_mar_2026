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
 * Entity class for ems_candidate_institute_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_candidate_institute_link")
public class CandidateInstituteLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("institution_id")
    private Long institutionId;
    
    @Column("comment")
    private String comment;
    
    @Column("status")
    private String status;
    
}
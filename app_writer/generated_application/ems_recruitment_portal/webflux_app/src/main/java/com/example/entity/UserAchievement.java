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
 * Entity class for ems_user_achievement table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_achievement")
public class UserAchievement {
    
    @Id
    @Column("achievement_id")
    private Long achievementId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("title")
    private String title;
    
    @Column("description")
    private String description;
    
    @Column("achievement_type")
    private String achievementType;
    
    @Column("issuer")
    private String issuer;
    
    @Column("date_achieved")
    private LocalDate dateAchieved;
    
    @Column("url")
    private String url;
    
    @Column("document_id")
    private Long documentId;
    
}
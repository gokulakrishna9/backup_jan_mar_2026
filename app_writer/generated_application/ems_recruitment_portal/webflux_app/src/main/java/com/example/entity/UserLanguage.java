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
 * Entity class for ems_user_language table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_language")
public class UserLanguage {
    
    @Id
    @Column("language_id")
    private Long languageId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("language_name")
    private String languageName;
    
    @Column("proficiency_level")
    private String proficiencyLevel;
    
    @Column("can_read")
    private Byte canRead;
    
    @Column("can_write")
    private Byte canWrite;
    
    @Column("can_speak")
    private Byte canSpeak;
    
}
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
 * Entity class for user_profile table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user_profile")
public class UserProfile {
    
    @Id
    @Column("user_profile_id")
    private Long userProfileId;
    
    @Column("first_name")
    private String firstname;
    
    @Column("last_name")
    private String lastname;
    
    @Column("email")
    private String email;
    
    @Column("phone")
    private String phone;
    
    @Column("bio")
    private String bio;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
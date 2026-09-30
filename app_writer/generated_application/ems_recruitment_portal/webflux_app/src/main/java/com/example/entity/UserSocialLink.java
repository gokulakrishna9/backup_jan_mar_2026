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
 * Entity class for ems_user_social_link table.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user_social_link")
public class UserSocialLink {
    
    @Id
    @Column("link_id")
    private Long linkId;
    
    @Column("user_id")
    private Long userId;
    
    @Column("platform")
    private String platform;
    
    @Column("profile_url")
    private String profileUrl;
    
    @Column("is_verified")
    private Byte isVerified;
    
}
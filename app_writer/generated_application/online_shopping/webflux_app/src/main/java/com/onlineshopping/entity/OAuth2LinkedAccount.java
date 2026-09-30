package com.onlineshopping.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Column;
import org.springframework.data.relational.core.mapping.Table;

import java.time.LocalDateTime;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Table("oauth2_linked_account")
public class OAuth2LinkedAccount {
    
    @Id
    @Column("linked_account_id")
    private Long linkedAccountId;
    
    @Column("auth_user_id")
    private Long authUserId;
    
    @Column("provider_id")
    private Long providerId;
    
    @Column("provider_user_id")
    private String providerUserId;
    
    @Column("provider_username")
    private String providerUsername;
    
    @Column("provider_email")
    private String providerEmail;
    
    @Column("access_token")
    private String accessToken;
    
    @Column("refresh_token")
    private String refreshToken;
    
    @Column("token_expires_at")
    private LocalDateTime tokenExpiresAt;
    
    @Column("linked_at")
    private LocalDateTime linkedAt;
    
    @Column("last_login_at")
    private LocalDateTime lastLoginAt;
}
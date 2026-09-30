package com.example.entity;

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
@Table("oauth2_provider")
public class OAuth2Provider {
    
    @Id
    @Column("provider_id")
    private Long providerId;
    
    @Column("provider_name")
    private String providerName;
    
    @Column("display_name")
    private String displayName;
    
    @Column("client_id")
    private String clientId;
    
    @Column("client_secret")
    private String clientSecret;
    
    @Column("authorization_uri")
    private String authorizationUri;
    
    @Column("token_uri")
    private String tokenUri;
    
    @Column("user_info_uri")
    private String userInfoUri;
    
    @Column("jwk_set_uri")
    private String jwkSetUri;
    
    @Column("issuer_uri")
    private String issuerUri;
    
    @Column("scope")
    private String scope;
    
    @Column("is_enabled")
    private Boolean isEnabled;
    
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
}
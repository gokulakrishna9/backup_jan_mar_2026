package com.example.auth;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import lombok.Getter;

@Configuration
@Getter
public class JwtConfig {
    
    @Value("${jwt.secret:your-secret-key-change-in-production}")
    private String secret;
    
    @Value("${jwt.expiration:86400000}")
    private Long expiration;
    
    @Value("${jwt.refresh-expiration:604800000}")
    private Long refreshExpiration;
}
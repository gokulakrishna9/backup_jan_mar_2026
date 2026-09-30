package com.example.entity;

import org.springframework.data.annotation.Id;
import org.springframework.data.relational.core.mapping.Table;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table("auth_user")
public class AuthUser {
    
    @Id
    private Long authUserId;
    private String username;
    private String email;
    private String passwordHash;
    private Boolean isActive;
    private LocalDateTime createdAt;
    private LocalDateTime updatedAt;
    
    @org.springframework.data.annotation.Transient
    private java.util.List<String> roles;
}
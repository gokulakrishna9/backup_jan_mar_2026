package com.onlineshopping.entity;

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
 * Entity class for user table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "user")
public class User {
    
    @Id
    @Column("user_id")
    private Long userId;
    
    @Column("username")
    private String username;
    
    @Column("encrypted_password")
    private String encryptedpassword;
    
    @Column("email")
    private String email;
    
    @Column("first_name")
    private String firstname;
    
    @Column("last_name")
    private String lastname;
    
    @Column("phone")
    private String phone;
    
    @Column("role")
    private String role;
    
    // Audit columns
    @Column("created_at")
    private LocalDateTime createdAt;
    
    @Column("updated_at")
    private LocalDateTime updatedAt;
    
}
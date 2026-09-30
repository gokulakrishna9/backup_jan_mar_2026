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
 * Entity class for ems_user table.
 * Root entity with authorization support.
 */
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table(name = "ems_user")
public class User {
    
    @Id
    @Column("user_id")
    private Long userId;
    
    @Column("first_name")
    private String firstName;
    
    @Column("last_name")
    private String lastName;
    
    @Column("gender")
    private String gender;
    
    @Column("date_of_birth")
    private LocalDate dateOfBirth;
    
    @Column("email_address")
    private String emailAddress;
    
    @Column("user_name")
    private String userName;
    
    @Column("encrypted_password")
    private String encryptedPassword;
    
    @Column("phone_number")
    private String phoneNumber;
    
    @Column("profile_photo")
    private String profilePhoto;
    
    @Column("is_active")
    private Byte isActive;
    
    @Column("is_entity")
    private Byte isEntity;
    
    @Column("is_public")
    private Boolean isPublic;
    
}
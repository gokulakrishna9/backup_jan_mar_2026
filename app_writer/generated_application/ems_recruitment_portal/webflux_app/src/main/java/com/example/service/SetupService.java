package com.example.service;

import com.example.entity.SystemConfig;
import com.example.entity.AuthUser;
import com.example.entity.UserRole;
import com.example.repository.SystemConfigRepository;
import com.example.repository.AuthUserRepository;
import com.example.repository.UserRoleRepository;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.time.LocalDateTime;

@Service
@RequiredArgsConstructor
public class SetupService {
    
    private final SystemConfigRepository systemConfigRepository;
    private final AuthUserRepository authUserRepository;
    private final UserRoleRepository userRoleRepository;
    private final PasswordEncoder passwordEncoder;
    
    /**
     * Check if initial setup has been completed
     */
    public Mono<Boolean> isSetupCompleted() {
        return systemConfigRepository.findByConfigKey("setup_completed")
            .map(config -> "true".equalsIgnoreCase(config.getConfigValue()))
            .defaultIfEmpty(false);
    }
    
    /**
     * Create super user and mark setup as completed
     */
    @Transactional
    public Mono<Void> createSuperUser(String username, String email, String password) {
        // Check if username already exists
        return authUserRepository.existsByUsername(username)
            .flatMap(exists -> {
                if (exists) {
                    return Mono.error(new RuntimeException("Username already exists"));
                }
                return authUserRepository.existsByEmail(email);
            })
            .flatMap(exists -> {
                if (exists) {
                    return Mono.error(new RuntimeException("Email already exists"));
                }
                
                // Create super user
                AuthUser superUser = AuthUser.builder()
                    .username(username)
                    .email(email)
                    .passwordHash(passwordEncoder.encode(password))
                    .isActive(true)
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return authUserRepository.save(superUser);
            })
            .flatMap(savedUser -> {
                // Assign SUPER_ADMIN role
                UserRole superAdminRole = UserRole.builder()
                    .authUserId(savedUser.getAuthUserId())
                    .role("SUPER_ADMIN")
                    .grantedAt(LocalDateTime.now())
                    .grantedByAuthUserId(savedUser.getAuthUserId())
                    .build();
                return userRoleRepository.save(superAdminRole)
                    .thenReturn(savedUser);
            })
            .flatMap(savedUser -> {
                // Mark setup as completed
                return systemConfigRepository.findByConfigKey("setup_completed")
                    .flatMap(config -> {
                        config.setConfigValue("true");
                        config.setUpdatedAt(LocalDateTime.now());
                        return systemConfigRepository.save(config);
                    })
                    .switchIfEmpty(
                        systemConfigRepository.save(
                            SystemConfig.builder()
                                .configKey("setup_completed")
                                .configValue("true")
                                .createdAt(LocalDateTime.now())
                                .updatedAt(LocalDateTime.now())
                                .build()
                        )
                    );
            })
            .then();
    }
}
package com.onlineshopping.service;

import com.onlineshopping.entity.AuthUser;
import com.onlineshopping.entity.QueryGroup;
import com.onlineshopping.entity.QueryGroupMember;
import com.onlineshopping.entity.QueryGroupQuery;
import com.onlineshopping.entity.UserRole;
import com.onlineshopping.repository.AuthUserRepository;
import com.onlineshopping.repository.QueryGroupRepository;
import com.onlineshopping.repository.QueryGroupMemberRepository;
import com.onlineshopping.repository.QueryGroupQueryRepository;
import com.onlineshopping.repository.UserRoleRepository;
import com.onlineshopping.auth.JwtService;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final AuthUserRepository authUserRepository;
    private final UserRoleRepository userRoleRepository;
    private final QueryGroupRepository queryGroupRepository;
    private final QueryGroupMemberRepository queryGroupMemberRepository;
    private final QueryGroupQueryRepository queryGroupQueryRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtService jwtService;
    private final ActivityTrackingService activityTrackingService;
    
    /**
     * Authenticate user and generate JWT token
     */
    public Mono<LoginResponse> login(String username, String password, ServerWebExchange exchange) {
        String ipAddress = getIpAddress(exchange);
        String userAgent = getUserAgent(exchange);
        String sessionId = UUID.randomUUID().toString();
        
        return authUserRepository.findByUsername(username)
            .switchIfEmpty(Mono.defer(() -> {
                // Log failed login - user not found
                return activityTrackingService.logFailedLogin(
                        username, ipAddress, userAgent, "User not found", "PASSWORD")
                    .then(Mono.error(new RuntimeException("Invalid username or password")));
            }))
            .flatMap(user -> {
                // Check if user is active
                if (!user.getIsActive()) {
                    return activityTrackingService.logFailedLogin(
                            username, ipAddress, userAgent, "Account inactive", "PASSWORD")
                        .then(Mono.error(new RuntimeException("User account is inactive")));
                }
                
                // Verify password
                if (!passwordEncoder.matches(password, user.getPasswordHash())) {
                    return activityTrackingService.logFailedLogin(
                            username, ipAddress, userAgent, "Invalid password", "PASSWORD")
                        .then(Mono.error(new RuntimeException("Invalid username or password")));
                }
                
                // Load roles and query group memberships, then generate JWT
                return buildJwtClaims(user)
                    .flatMap(claims -> {
                        String token = jwtService.generateToken(user.getUsername(), user.getAuthUserId(),
                            claims.roles(), claims.tableAccess(), claims.queryGroupMemberships());
                        String refreshToken = jwtService.generateRefreshToken(user.getUsername(), user.getAuthUserId());
                        
                        log.info("User logged in successfully: {}", username);
                        
                        // Log successful login
                        return activityTrackingService.logLogin(
                                user.getAuthUserId(), username, ipAddress, userAgent, 
                                sessionId, "PASSWORD", null)
                            .thenReturn(new LoginResponse(
                                token,
                                refreshToken,
                                user.getAuthUserId(),
                                user.getUsername(),
                                user.getEmail()
                            ));
                    });
            });
    }
    
    /**
     * Authenticate user and generate JWT token (without exchange - for backward compatibility)
     */
    public Mono<LoginResponse> login(String username, String password) {
        return authUserRepository.findByUsername(username)
            .switchIfEmpty(Mono.error(new RuntimeException("Invalid username or password")))
            .flatMap(user -> {
                if (!user.getIsActive()) {
                    return Mono.error(new RuntimeException("User account is inactive"));
                }
                if (!passwordEncoder.matches(password, user.getPasswordHash())) {
                    return Mono.error(new RuntimeException("Invalid username or password"));
                }
                return buildJwtClaims(user)
                    .map(claims -> {
                        String token = jwtService.generateToken(user.getUsername(), user.getAuthUserId(),
                            claims.roles(), claims.tableAccess(), claims.queryGroupMemberships());
                        String refreshToken = jwtService.generateRefreshToken(user.getUsername(), user.getAuthUserId());
                        log.info("User logged in successfully: {}", username);
                        return new LoginResponse(
                            token, refreshToken, user.getAuthUserId(), user.getUsername(), 
                            user.getEmail()
                        );
                    });
            });
    }
    
    private String getIpAddress(ServerWebExchange exchange) {
        if (exchange == null) return "unknown";
        String ip = exchange.getRequest().getHeaders().getFirst("X-Forwarded-For");
        if (ip == null || ip.isEmpty()) {
            ip = exchange.getRequest().getRemoteAddress() != null 
                ? exchange.getRequest().getRemoteAddress().getAddress().getHostAddress() 
                : "unknown";
        }
        return ip;
    }
    
    private String getUserAgent(ServerWebExchange exchange) {
        if (exchange == null) return "unknown";
        return exchange.getRequest().getHeaders().getFirst("User-Agent");
    }
    
    /**
     * Register new user
     */
    public Mono<RegisterResponse> register(String username, String email, String password) {
        // Validate inputs
        if (username == null || username.trim().isEmpty()) {
            return Mono.error(new RuntimeException("Username is required"));
        }
        if (email == null || email.trim().isEmpty()) {
            return Mono.error(new RuntimeException("Email is required"));
        }
        if (password == null || password.length() < 8) {
            return Mono.error(new RuntimeException("Password must be at least 8 characters"));
        }
        
        // Check if username exists
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
                
                // Create new user
                AuthUser newUser = AuthUser.builder()
                    .username(username)
                    .email(email)
                    .passwordHash(passwordEncoder.encode(password))
                    .isActive(true)
                    .createdAt(LocalDateTime.now())
                    .updatedAt(LocalDateTime.now())
                    .build();
                
                return authUserRepository.save(newUser);
            })
            .flatMap(savedUser -> {
                log.info("User registered successfully: {}", username);
                
                // Assign default USER role
                UserRole defaultRole = UserRole.builder()
                    .authUserId(savedUser.getAuthUserId())
                    .role("USER")
                    .grantedAt(LocalDateTime.now())
                    .build();
                
                return userRoleRepository.save(defaultRole)
                    .then(Mono.defer(() -> {
                        // Create Community query group for the new user
                        QueryGroup communityGroup = QueryGroup.builder()
                            .groupName("community_" + savedUser.getUsername())
                            .groupType("COMMUNITY")
                            .ownerAuthUserId(savedUser.getAuthUserId())
                            .description("Community group for " + savedUser.getUsername())
                            .createdAt(LocalDateTime.now())
                            .build();
                        
                        return queryGroupRepository.save(communityGroup)
                            .flatMap(savedGroup -> {
                                // Add user as member of the Community group
                                QueryGroupMember member = QueryGroupMember.builder()
                                    .queryGroupId(savedGroup.getQueryGroupId())
                                    .authUserId(savedUser.getAuthUserId())
                                    .joinedAt(LocalDateTime.now())
                                    .build();
                                
                                return queryGroupMemberRepository.save(member)
                                    .then(populateCommunityDefaultQueries(savedGroup.getQueryGroupId()))
                                    .thenReturn(savedUser);
                            });
                    }));
            })
            .map(savedUser -> new RegisterResponse(
                savedUser.getAuthUserId(),
                savedUser.getUsername(),
                savedUser.getEmail(),
                "User registered successfully"
            ));
    }
    
    /**
     * Get current authenticated user
     */
    public Mono<AuthUser> getCurrentUser(Long authUserId) {
        return authUserRepository.findById(authUserId)
            .switchIfEmpty(Mono.error(new RuntimeException("User not found")));
    }
    
    /**
     * Validate JWT token and extract user
     */
    public Mono<AuthUser> validateToken(String token) {
        try {
            if (!jwtService.validateToken(token)) {
                return Mono.error(new RuntimeException("Invalid token"));
            }
            
            String username = jwtService.extractUsername(token);
            return authUserRepository.findByUsername(username)
                .switchIfEmpty(Mono.error(new RuntimeException("User not found")));
        } catch (Exception e) {
            return Mono.error(new RuntimeException("Token validation failed: " + e.getMessage()));
        }
    }
    
    /**
     * Change user password
     */
    public Mono<Void> changePassword(Long authUserId, String oldPassword, String newPassword) {
        if (newPassword == null || newPassword.length() < 8) {
            return Mono.error(new RuntimeException("New password must be at least 8 characters"));
        }
        
        return authUserRepository.findById(authUserId)
            .switchIfEmpty(Mono.error(new RuntimeException("User not found")))
            .flatMap(user -> {
                // Verify old password
                if (!passwordEncoder.matches(oldPassword, user.getPasswordHash())) {
                    return Mono.error(new RuntimeException("Current password is incorrect"));
                }
                
                // Update password
                user.setPasswordHash(passwordEncoder.encode(newPassword));
                user.setUpdatedAt(LocalDateTime.now());
                
                return authUserRepository.save(user);
            })
            .then();
    }
    
    /**
     * Deactivate user account
     */
    public Mono<Void> deactivateUser(Long authUserId) {
        return authUserRepository.findById(authUserId)
            .switchIfEmpty(Mono.error(new RuntimeException("User not found")))
            .flatMap(user -> {
                user.setIsActive(false);
                user.setUpdatedAt(LocalDateTime.now());
                return authUserRepository.save(user);
            })
            .then();
    }
    
    /**
     * Refresh access token using a valid refresh token
     */
    public Mono<LoginResponse> refreshToken(String refreshToken) {
        if (!jwtService.validateRefreshToken(refreshToken)) {
            return Mono.error(new RuntimeException("Invalid or expired refresh token"));
        }
        
        String username = jwtService.extractUsername(refreshToken);
        Long userId = jwtService.extractUserId(refreshToken);
        
        return authUserRepository.findByUsername(username)
            .switchIfEmpty(Mono.error(new RuntimeException("User not found")))
            .flatMap(user -> {
                if (!user.getIsActive()) {
                    return Mono.error(new RuntimeException("User account is inactive"));
                }
                
                return buildJwtClaims(user)
                    .map(claims -> {
                        String newToken = jwtService.generateToken(user.getUsername(), user.getAuthUserId(),
                            claims.roles(), claims.tableAccess(), claims.queryGroupMemberships());
                        String newRefreshToken = jwtService.generateRefreshToken(user.getUsername(), user.getAuthUserId());
                        
                        log.info("Token refreshed for user: {}", username);
                        
                        return new LoginResponse(
                            newToken,
                            newRefreshToken,
                            user.getAuthUserId(),
                            user.getUsername(),
                            user.getEmail()
                        );
                    });
            });
    }
    
    /**
     * Build JWT claims (roles, tableAccess, queryGroupMemberships) from the database for a given user.
     */
    private Mono<JwtClaims> buildJwtClaims(AuthUser user) {
        Mono<List<UserRole>> rolesMono = userRoleRepository.findByAuthUserId(user.getAuthUserId())
            .collectList();
        Mono<List<QueryGroupMember>> membershipsMono = queryGroupMemberRepository.findByAuthUserId(user.getAuthUserId())
            .collectList();
        
        return Mono.zip(rolesMono, membershipsMono)
            .map(tuple -> {
                List<UserRole> userRoles = tuple.getT1();
                List<QueryGroupMember> memberships = tuple.getT2();
                
                // Build roles claim: List<Map<String, Object>> with "role" and "tableName"
                List<Map<String, Object>> roles = userRoles.stream()
                    .map(ur -> {
                        Map<String, Object> roleMap = new HashMap<>();
                        roleMap.put("role", ur.getRole());
                        roleMap.put("tableName", ur.getTableName());
                        return roleMap;
                    })
                    .collect(Collectors.toList());
                
                // Build tableAccess claim: Map<String, List<String>>
                // SUPER_ADMIN: handled by WebFilter via isSuperAdmin() check on roles — no tableAccess entries needed
                // TABLE_ADMIN: each assigned table gets all CRUD ops
                // USER: no tableAccess entries (access handled by record ownership at service layer)
                Map<String, List<String>> tableAccess = new HashMap<>();
                List<String> allOps = List.of("CREATE", "READ", "UPDATE", "DELETE");
                for (UserRole ur : userRoles) {
                    if ("TABLE_ADMIN".equals(ur.getRole()) && ur.getTableName() != null) {
                        tableAccess.put(ur.getTableName(), allOps);
                    }
                }
                
                // Build queryGroupMemberships claim: List<Long>
                List<Long> queryGroupMemberships = memberships.stream()
                    .map(QueryGroupMember::getQueryGroupId)
                    .collect(Collectors.toList());
                
                return new JwtClaims(roles, tableAccess, queryGroupMemberships);
            });
    }
    
    /**
     * Internal record holding pre-built JWT claims.
     */
    private record JwtClaims(
        List<Map<String, Object>> roles,
        Map<String, List<String>> tableAccess,
        List<Long> queryGroupMemberships
    ) {}
    
    /**
     * Populate a Community group with community-default queries from the app definition.
     */
    private Mono<Void> populateCommunityDefaultQueries(Long queryGroupId) {
        List<String> communityDefaultQueries = getCommunityDefaultQueryNames();
        if (communityDefaultQueries.isEmpty()) {
            return Mono.empty();
        }
        return Flux.fromIterable(communityDefaultQueries)
            .flatMap(queryName -> {
                QueryGroupQuery groupQuery = QueryGroupQuery.builder()
                    .queryGroupId(queryGroupId)
                    .queryName(queryName)
                    .build();
                return queryGroupQueryRepository.save(groupQuery);
            })
            .then();
    }
    
    /**
     * Get community-default query names from the app definition.
     * Override this method to provide app-specific community-default queries.
     */
    protected List<String> getCommunityDefaultQueryNames() {
        return List.of();
    }
    
    // DTOs
    public record LoginResponse(
        String token,
        String refreshToken,
        Long userId,
        String username,
        String email
    ) {}
    
    public record RegisterResponse(
        Long userId,
        String username,
        String email,
        String message
    ) {}
}
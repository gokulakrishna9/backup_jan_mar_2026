"""Authentication service templates for code generation."""


class AuthServiceTemplates:
    """Templates for authentication service generation."""
    
    # Auth Service
    AUTH_SERVICE = """package {{ packageName }};

import {{ entityPackage }}.AuthUser;
import {{ entityPackage }}.QueryGroup;
import {{ entityPackage }}.QueryGroupMember;
import {{ entityPackage }}.QueryGroupQuery;
import {{ entityPackage }}.UserRole;
import {{ repositoryPackage }}.AuthUserRepository;
import {{ repositoryPackage }}.QueryGroupRepository;
import {{ repositoryPackage }}.QueryGroupMemberRepository;
import {{ repositoryPackage }}.QueryGroupQueryRepository;
import {{ repositoryPackage }}.UserRoleRepository;
import {{ authPackage }}.JwtService;
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
"""

    # Updated Auth Controller
    AUTH_CONTROLLER_UPDATED = """package {{ packageName }};

import {{ servicePackage }}.AuthService;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    
    private final AuthService authService;
    
    @PostMapping("/login")
    public Mono<AuthService.LoginResponse> login(@RequestBody LoginRequest request, ServerWebExchange exchange) {
        return authService.login(request.username(), request.password(), exchange);
    }
    
    @PostMapping("/register")
    public Mono<AuthService.RegisterResponse> register(@RequestBody RegisterRequest request) {
        return authService.register(
            request.username(),
            request.email(),
            request.password()
        );
    }
    
    @PostMapping("/refresh")
    public Mono<AuthService.LoginResponse> refresh(@RequestBody RefreshRequest request) {
        return authService.refreshToken(request.refreshToken());
    }
    
    @PostMapping("/change-password")
    public Mono<ChangePasswordResponse> changePassword(
            @RequestHeader("Authorization") String authHeader,
            @RequestBody ChangePasswordRequest request) {
        // Extract token from "Bearer <token>"
        String token = authHeader.substring(7);
        
        return authService.validateToken(token)
            .flatMap(user -> authService.changePassword(
                user.getAuthUserId(),
                request.oldPassword(),
                request.newPassword()
            ))
            .then(Mono.just(new ChangePasswordResponse("Password changed successfully")));
    }
    
    @GetMapping("/me")
    public Mono<UserInfoResponse> getCurrentUser(@RequestHeader("Authorization") String authHeader) {
        // Extract token from "Bearer <token>"
        String token = authHeader.substring(7);
        
        return authService.validateToken(token)
            .map(user -> new UserInfoResponse(
                user.getAuthUserId(),
                user.getUsername(),
                user.getEmail(),
                user.getIsActive()
            ));
    }
    
    // Request/Response DTOs
    record LoginRequest(String username, String password) {}
    record RegisterRequest(String username, String password, String email) {}
    record RefreshRequest(String refreshToken) {}
    record ChangePasswordRequest(String oldPassword, String newPassword) {}
    record ChangePasswordResponse(String message) {}
    record UserInfoResponse(Long userId, String username, String email, Boolean isActive) {}
}
"""

    # JWT Authentication Filter
    JWT_AUTHENTICATION_FILTER = """package {{ packageName }};

import {{ authPackage }}.JwtService;
import {{ servicePackage }}.AuthService;
import {{ exceptionPackage }}.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.web.server.ServerWebExchange;
import org.springframework.web.server.WebFilter;
import org.springframework.web.server.WebFilterChain;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@Slf4j
@RequiredArgsConstructor
public class JwtAuthenticationFilter implements WebFilter {
    
    private final JwtService jwtService;
    private final AuthService authService;
    private final ObjectMapper objectMapper;
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, WebFilterChain chain) {
        ServerHttpRequest request = exchange.getRequest();
        String path = request.getPath().value();
        
        // Skip authentication for public endpoints
        if (isPublicEndpoint(path)) {
            return chain.filter(exchange);
        }
        
        // Extract JWT token from Authorization header
        String authHeader = request.getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
        
        // Missing Authorization header
        if (authHeader == null || authHeader.trim().isEmpty()) {
            log.warn("Missing Authorization header for path: {}", path);
            return writeUnauthorizedResponse(exchange, "MISSING_TOKEN", 
                "Authorization header is required", path);
        }
        
        // Invalid Authorization header format
        if (!authHeader.startsWith("Bearer ")) {
            log.warn("Invalid Authorization header format for path: {}", path);
            return writeUnauthorizedResponse(exchange, "INVALID_TOKEN_FORMAT", 
                "Authorization header must start with 'Bearer '", path);
        }
        
        String token = authHeader.substring(7).trim();
        
        // Empty token
        if (token.isEmpty()) {
            log.warn("Empty JWT token for path: {}", path);
            return writeUnauthorizedResponse(exchange, "EMPTY_TOKEN", 
                "JWT token is required", path);
        }
        
        // Validate token and set security context
        return authService.validateToken(token)
            .flatMap(user -> {
                // Extract roles from JWT and set on user (transient field)
                List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
                if (roleObjects != null) {
                    user.setRoles(roleObjects.stream()
                        .map(r -> r.get("role") != null ? r.get("role").toString() : "")
                        .collect(java.util.stream.Collectors.toList()));
                } else {
                    user.setRoles(List.of());
                }

                // Create authentication with authorities
                List<SimpleGrantedAuthority> authorities = List.of(new SimpleGrantedAuthority("ROLE_USER"));
                
                UsernamePasswordAuthenticationToken authentication =
                    new UsernamePasswordAuthenticationToken(user, null, authorities);
                
                // Set security context and continue filter chain
                return chain.filter(exchange)
                    .contextWrite(ReactiveSecurityContextHolder.withAuthentication(authentication));
            })
            .onErrorResume(e -> {
                // Token validation failed - return 401
                log.warn("JWT token validation failed for path {}: {}", path, e.getMessage());
                return writeUnauthorizedResponse(exchange, "INVALID_TOKEN", 
                    "Invalid or expired JWT token", path);
            });
    }
    
    private Mono<Void> writeUnauthorizedResponse(ServerWebExchange exchange, String errorCode, 
                                                  String message, String path) {
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.UNAUTHORIZED);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.UNAUTHORIZED.value())
            .error(HttpStatus.UNAUTHORIZED.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode(errorCode)
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write error response", e);
            return response.setComplete();
        }
    }
    
    private boolean isPublicEndpoint(String path) {
        return path.startsWith("/api/auth/login") ||
               path.startsWith("/api/auth/register") ||
               path.startsWith("/api/auth/refresh") ||
               path.startsWith("/setup") ||
               path.startsWith("/login") ||
               path.startsWith("/swagger-ui") ||
               path.startsWith("/v3/api-docs") ||
               path.startsWith("/webjars") ||
               path.startsWith("/favicon") ||
               path.equals("/");
    }
}
"""

    # Security Context Holder Utility
    SECURITY_CONTEXT_HOLDER = """package {{ packageName }};

import {{ entityPackage }}.AuthUser;
import {{ authPackage }}.JwtService;
import {{ repositoryPackage }}.AuthUserRepository;
import org.springframework.http.HttpHeaders;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.ReactiveSecurityContextHolder;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

public class SecurityContextHolder {
    
    /**
     * Get current authenticated user from security context
     */
    public static Mono<AuthUser> getCurrentUser() {
        return ReactiveSecurityContextHolder.getContext()
            .map(context -> context.getAuthentication())
            .filter(auth -> auth instanceof UsernamePasswordAuthenticationToken)
            .map(auth -> (AuthUser) auth.getPrincipal())
            .switchIfEmpty(Mono.error(new RuntimeException("No authenticated user found")));
    }
    
    /**
     * Get current authenticated user, falling back to JWT in exchange header.
     */
    public static Mono<AuthUser> getCurrentUser(ServerWebExchange exchange, JwtService jwtService,
                                                 AuthUserRepository authUserRepository) {
        return ReactiveSecurityContextHolder.getContext()
            .map(context -> context.getAuthentication())
            .filter(auth -> auth instanceof UsernamePasswordAuthenticationToken)
            .map(auth -> (AuthUser) auth.getPrincipal())
            .switchIfEmpty(Mono.defer(() -> {
                if (exchange == null) {
                    return Mono.error(new RuntimeException("No authenticated user found"));
                }
                String authHeader = exchange.getRequest().getHeaders().getFirst(HttpHeaders.AUTHORIZATION);
                if (authHeader == null || !authHeader.startsWith("Bearer ")) {
                    return Mono.error(new RuntimeException("No authenticated user found"));
                }
                String token = authHeader.substring(7).trim();
                String username = jwtService.extractUsername(token);
                if (username == null) {
                    return Mono.error(new RuntimeException("Invalid JWT token"));
                }
                return authUserRepository.findByUsername(username)
                    .map(user -> {
                        List<Map<String, Object>> roleObjects = jwtService.extractRoles(token);
                        if (roleObjects != null) {
                            user.setRoles(roleObjects.stream()
                                .map(r -> r.get("role") != null ? r.get("role").toString() : "")
                                .collect(Collectors.toList()));
                        } else {
                            user.setRoles(List.of());
                        }
                        return user;
                    })
                    .switchIfEmpty(Mono.error(new RuntimeException("User not found")));
            }));
    }
    
    /**
     * Get current user ID
     */
    public static Mono<Long> getCurrentUserId() {
        return getCurrentUser()
            .map(AuthUser::getAuthUserId);
    }
}
"""

    # Authorization Denied Handler for 403 responses
    AUTHORIZATION_DENIED_HANDLER = """package {{ packageName }};

import {{ exceptionPackage }}.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.server.reactive.ServerHttpResponse;
import org.springframework.stereotype.Component;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.time.LocalDateTime;

/**
 * Handles authorization denied (403 Forbidden) responses.
 * Used when a user is authenticated but lacks permission for the requested resource.
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class AuthorizationDeniedHandler {
    
    private final ObjectMapper objectMapper;
    
    /**
     * Write a 403 Forbidden response with detailed error information.
     */
    public Mono<Void> handle(ServerWebExchange exchange, String operation, String resource) {
        String path = exchange.getRequest().getPath().value();
        log.warn("Access denied for operation '{}' on resource '{}' at path: {}", operation, resource, path);
        
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.FORBIDDEN);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        String message = String.format("Access denied: insufficient permissions for %s on %s", operation, resource);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.FORBIDDEN.value())
            .error(HttpStatus.FORBIDDEN.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode("ACCESS_DENIED")
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write forbidden response", e);
            return response.setComplete();
        }
    }
    
    /**
     * Write a generic 403 Forbidden response.
     */
    public Mono<Void> handleGeneric(ServerWebExchange exchange, String message) {
        String path = exchange.getRequest().getPath().value();
        log.warn("Access denied at path {}: {}", path, message);
        
        ServerHttpResponse response = exchange.getResponse();
        response.setStatusCode(HttpStatus.FORBIDDEN);
        response.getHeaders().setContentType(MediaType.APPLICATION_JSON);
        
        ErrorResponse errorResponse = ErrorResponse.builder()
            .timestamp(LocalDateTime.now())
            .status(HttpStatus.FORBIDDEN.value())
            .error(HttpStatus.FORBIDDEN.getReasonPhrase())
            .message(message)
            .path(path)
            .errorCode("ACCESS_DENIED")
            .build();
        
        try {
            byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
            DataBuffer buffer = response.bufferFactory().wrap(bytes);
            return response.writeWith(Mono.just(buffer));
        } catch (Exception e) {
            log.error("Failed to write forbidden response", e);
            return response.setComplete();
        }
    }
}
"""

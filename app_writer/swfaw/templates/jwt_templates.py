"""JWT templates for code generation."""


class JWTTemplates:
    """Templates for JWT authentication generation."""
    
    JWT_CONFIG_TEMPLATE = """package {{ packageName }};

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import lombok.Getter;

@Configuration
@Getter
public class JwtConfig {
    
    @Value("${jwt.secret:{{ jwtSecret }}}")
    private String secret;
    
    @Value("${jwt.expiration:{{ jwtExpiration }}}")
    private Long expiration;
    
    @Value("${jwt.refresh-expiration:{{ refreshExpiration }}}")
    private Long refreshExpiration;
}
"""
    
    JWT_SERVICE_TEMPLATE = """package {{ packageName }};

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import org.springframework.stereotype.Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import java.util.*;
import java.util.stream.Collectors;
import javax.crypto.SecretKey;

@Slf4j
@Service
@RequiredArgsConstructor
public class JwtService {
    
    private final JwtConfig jwtConfig;
    private final ObjectMapper objectMapper = new ObjectMapper();
    
    public String generateToken(String username, Long userId,
                                List<Map<String, Object>> roles,
                                Map<String, List<String>> tableAccess,
                                List<Long> queryGroupMemberships) {
        SecretKey key = Keys.hmacShaKeyFor(jwtConfig.getSecret().getBytes());
        
        try {
            String rolesJson = objectMapper.writeValueAsString(roles != null ? roles : Collections.emptyList());
            String tableAccessJson = objectMapper.writeValueAsString(tableAccess != null ? tableAccess : Collections.emptyMap());
            String queryGroupMembershipsJson = objectMapper.writeValueAsString(queryGroupMemberships != null ? queryGroupMemberships : Collections.emptyList());
            
            return Jwts.builder()
                .setSubject(username)
                .claim("userId", userId)
                .claim("roles", rolesJson)
                .claim("tableAccess", tableAccessJson)
                .claim("queryGroupMemberships", queryGroupMembershipsJson)
                .setIssuedAt(new Date())
                .setExpiration(new Date(System.currentTimeMillis() + jwtConfig.getExpiration()))
                .signWith(key, SignatureAlgorithm.HS256)
                .compact();
        } catch (JsonProcessingException e) {
            log.error("Failed to serialize JWT claims", e);
            throw new RuntimeException("Failed to generate token", e);
        }
    }
    
    public String generateRefreshToken(String username, Long userId) {
        SecretKey key = Keys.hmacShaKeyFor(jwtConfig.getSecret().getBytes());
        
        return Jwts.builder()
            .setSubject(username)
            .claim("userId", userId)
            .claim("type", "refresh")
            .setIssuedAt(new Date())
            .setExpiration(new Date(System.currentTimeMillis() + jwtConfig.getRefreshExpiration()))
            .signWith(key, SignatureAlgorithm.HS256)
            .compact();
    }
    
    public String extractUsername(String token) {
        return getClaims(token).getSubject();
    }
    
    public boolean validateToken(String token) {
        try {
            getClaims(token);
            return true;
        } catch (Exception e) {
            return false;
        }
    }
    
    public boolean validateRefreshToken(String token) {
        try {
            Claims claims = getClaims(token);
            return "refresh".equals(claims.get("type", String.class));
        } catch (Exception e) {
            return false;
        }
    }
    
    public Long extractUserId(String token) {
        return getClaims(token).get("userId", Long.class);
    }
    
    public List<Map<String, Object>> extractRoles(String token) {
        try {
            String rolesJson = getClaims(token).get("roles", String.class);
            if (rolesJson == null || rolesJson.isEmpty()) {
                return Collections.emptyList();
            }
            return objectMapper.readValue(rolesJson, new TypeReference<List<Map<String, Object>>>() {});
        } catch (JsonProcessingException e) {
            log.error("Failed to parse roles from JWT", e);
            return Collections.emptyList();
        }
    }
    
    public Map<String, List<String>> extractTableAccess(String token) {
        try {
            String tableAccessJson = getClaims(token).get("tableAccess", String.class);
            if (tableAccessJson == null || tableAccessJson.isEmpty()) {
                return Collections.emptyMap();
            }
            return objectMapper.readValue(tableAccessJson, new TypeReference<Map<String, List<String>>>() {});
        } catch (JsonProcessingException e) {
            log.error("Failed to parse tableAccess from JWT", e);
            return Collections.emptyMap();
        }
    }
    
    public List<Long> extractQueryGroupMemberships(String token) {
        try {
            String membershipsJson = getClaims(token).get("queryGroupMemberships", String.class);
            if (membershipsJson == null || membershipsJson.isEmpty()) {
                return Collections.emptyList();
            }
            return objectMapper.readValue(membershipsJson, new TypeReference<List<Long>>() {});
        } catch (JsonProcessingException e) {
            log.error("Failed to parse queryGroupMemberships from JWT", e);
            return Collections.emptyList();
        }
    }
    
    private Claims getClaims(String token) {
        SecretKey key = Keys.hmacShaKeyFor(jwtConfig.getSecret().getBytes());
        return Jwts.parserBuilder()
            .setSigningKey(key)
            .build()
            .parseClaimsJws(token)
            .getBody();
    }
}
"""
    
    AUTH_CONTROLLER_TEMPLATE = """package {{ packageName }};

import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;
import java.util.Collections;

@RestController
@RequestMapping("/api/auth")
@RequiredArgsConstructor
public class AuthController {
    
    private final JwtService jwtService;
    
    @PostMapping("/login")
    public Mono<LoginResponse> login(@RequestBody LoginRequest request) {
        // TODO: Implement authentication logic
        // TODO: Load roles, tableAccess, queryGroupMemberships from database
        String token = jwtService.generateToken(request.username(), 1L,
            Collections.emptyList(), Collections.emptyMap(), Collections.emptyList());
        return Mono.just(new LoginResponse(token));
    }
    
    @PostMapping("/register")
    public Mono<RegisterResponse> register(@RequestBody RegisterRequest request) {
        // TODO: Implement registration logic
        return Mono.just(new RegisterResponse("User registered successfully"));
    }
    
    record LoginRequest(String username, String password) {}
    record LoginResponse(String token) {}
    record RegisterRequest(String username, String password, String email) {}
    record RegisterResponse(String message) {}
}
"""

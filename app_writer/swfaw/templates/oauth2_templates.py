"""Templates for OAuth2 authentication components."""

# OAuth2 Provider Entity
OAUTH2_PROVIDER_ENTITY = """package {{ entityPackage }};

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
"""

# OAuth2 Linked Account Entity
OAUTH2_LINKED_ACCOUNT_ENTITY = """package {{ entityPackage }};

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
"""

# OAuth2 Provider Repository
OAUTH2_PROVIDER_REPOSITORY = """package {{ repositoryPackage }};

import {{ entityPackage }}.OAuth2Provider;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface OAuth2ProviderRepository extends ReactiveCrudRepository<OAuth2Provider, Long> {
    
    Mono<OAuth2Provider> findByProviderName(String providerName);
    
    @Query("SELECT * FROM oauth2_provider WHERE is_enabled = true")
    Flux<OAuth2Provider> findAllEnabled();
}
"""

# OAuth2 Linked Account Repository
OAUTH2_LINKED_ACCOUNT_REPOSITORY = """package {{ repositoryPackage }};

import {{ entityPackage }}.OAuth2LinkedAccount;
import org.springframework.data.r2dbc.repository.Query;
import org.springframework.data.repository.reactive.ReactiveCrudRepository;
import org.springframework.stereotype.Repository;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Repository
public interface OAuth2LinkedAccountRepository extends ReactiveCrudRepository<OAuth2LinkedAccount, Long> {
    
    @Query("SELECT * FROM oauth2_linked_account WHERE auth_user_id = :authUserId")
    Flux<OAuth2LinkedAccount> findByAuthUserId(Long authUserId);
    
    @Query("SELECT * FROM oauth2_linked_account WHERE provider_id = :providerId AND provider_user_id = :providerUserId")
    Mono<OAuth2LinkedAccount> findByProviderAndUserId(Long providerId, String providerUserId);
    
    @Query("SELECT * FROM oauth2_linked_account WHERE provider_email = :email")
    Flux<OAuth2LinkedAccount> findByProviderEmail(String email);
}
"""

# OAuth2 Service
OAUTH2_SERVICE = """package {{ servicePackage }};

import {{ entityPackage }}.OAuth2Provider;
import {{ entityPackage }}.OAuth2LinkedAccount;
import {{ entityPackage }}.AuthUser;
import {{ repositoryPackage }}.OAuth2ProviderRepository;
import {{ repositoryPackage }}.OAuth2LinkedAccountRepository;
import {{ repositoryPackage }}.AuthUserRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.time.LocalDateTime;
import java.util.Map;

@Slf4j
@Service
@RequiredArgsConstructor
public class OAuth2Service {
    private final OAuth2ProviderRepository oauth2ProviderRepository;
    private final OAuth2LinkedAccountRepository linkedAccountRepository;
    private final AuthUserRepository authUserRepository;
    private final WebClient.Builder webClientBuilder;
    
    public Flux<OAuth2Provider> getEnabledProviders() {
        return oauth2ProviderRepository.findAllEnabled();
    }
    
    public Mono<OAuth2Provider> getProviderByName(String providerName) {
        return oauth2ProviderRepository.findByProviderName(providerName);
    }
    
    public Mono<String> generateAuthorizationUrl(String providerName, String state, String redirectUri) {
        return getProviderByName(providerName)
            .map(provider -> provider.getAuthorizationUri() + 
                "?client_id=" + provider.getClientId() +
                "&redirect_uri=" + (redirectUri != null ? redirectUri : "http://localhost:8081/api/oauth2/callback/" + providerName) +
                "&response_type=code&scope=" + provider.getScope() + "&state=" + state);
    }
    
    @SuppressWarnings("unchecked")
    public Mono<Map<String, Object>> exchangeCodeForToken(String providerName, String code, String redirectUri) {
        return getProviderByName(providerName)
            .flatMap(provider -> webClientBuilder.build().post()
                .uri(provider.getTokenUri())
                .header("Content-Type", "application/x-www-form-urlencoded")
                .bodyValue("grant_type=authorization_code&code=" + code + 
                    "&client_id=" + provider.getClientId() + 
                    "&client_secret=" + provider.getClientSecret() +
                    "&redirect_uri=" + (redirectUri != null ? redirectUri : "http://localhost:8081/api/oauth2/callback/" + providerName))
                .retrieve().bodyToMono(Map.class)
                .map(map -> (Map<String, Object>) map));
    }
    
    @SuppressWarnings("unchecked")
    public Mono<Map<String, Object>> getUserInfo(String providerName, String accessToken) {
        return getProviderByName(providerName)
            .flatMap(provider -> webClientBuilder.build().get()
                .uri(provider.getUserInfoUri())
                .header("Authorization", "Bearer " + accessToken)
                .retrieve().bodyToMono(Map.class)
                .map(map -> (Map<String, Object>) map));
    }
    
    public Mono<AuthUser> linkOrCreateUser(String providerName, Map<String, Object> userInfo, String accessToken, String refreshToken) {
        return getProviderByName(providerName)
            .flatMap(provider -> {
                String providerUserId = extractAttribute(userInfo, "sub", "id");
                String email = extractAttribute(userInfo, "email");
                String username = extractAttribute(userInfo, "login", "preferred_username", "email");
                
                return linkedAccountRepository.findByProviderAndUserId(provider.getProviderId(), providerUserId)
                    .flatMap(linkedAccount -> {
                        linkedAccount.setAccessToken(accessToken);
                        linkedAccount.setRefreshToken(refreshToken);
                        linkedAccount.setTokenExpiresAt(LocalDateTime.now().plusHours(1));
                        linkedAccount.setLastLoginAt(LocalDateTime.now());
                        return linkedAccountRepository.save(linkedAccount)
                            .flatMap(saved -> authUserRepository.findById(saved.getAuthUserId()));
                    })
                    .switchIfEmpty(createUserFromOAuth2(provider, providerUserId, username, email, accessToken, refreshToken));
            });
    }
    
    private Mono<AuthUser> createUserFromOAuth2(OAuth2Provider provider, String providerUserId, 
                                                  String username, String email, 
                                                  String accessToken, String refreshToken) {
        AuthUser newUser = new AuthUser();
        newUser.setUsername(username);
        newUser.setEmail(email);
        newUser.setPasswordHash(null);
        newUser.setIsActive(true);
        newUser.setCreatedAt(LocalDateTime.now());
        newUser.setUpdatedAt(LocalDateTime.now());
        
        return authUserRepository.save(newUser)
            .flatMap(savedUser -> {
                OAuth2LinkedAccount linkedAccount = new OAuth2LinkedAccount();
                linkedAccount.setAuthUserId(savedUser.getAuthUserId());
                linkedAccount.setProviderId(provider.getProviderId());
                linkedAccount.setProviderUserId(providerUserId);
                linkedAccount.setProviderUsername(username);
                linkedAccount.setProviderEmail(email);
                linkedAccount.setAccessToken(accessToken);
                linkedAccount.setRefreshToken(refreshToken);
                linkedAccount.setTokenExpiresAt(LocalDateTime.now().plusHours(1));
                linkedAccount.setLinkedAt(LocalDateTime.now());
                linkedAccount.setLastLoginAt(LocalDateTime.now());
                return linkedAccountRepository.save(linkedAccount).thenReturn(savedUser);
            });
    }
    
    private String extractAttribute(Map<String, Object> userInfo, String... keys) {
        for (String key : keys) {
            Object value = userInfo.get(key);
            if (value != null) return value.toString();
        }
        return null;
    }
}
"""

# OAuth2 Controller
OAUTH2_CONTROLLER = """package {{ controllerPackage }};

import {{ servicePackage }}.OAuth2Service;
import {{ authPackage }}.JwtService;
import {{ entityPackage }}.OAuth2Provider;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import java.util.Map;
import java.util.UUID;

@Slf4j
@RestController
@RequestMapping("/api/oauth2")
@RequiredArgsConstructor
public class OAuth2Controller {
    private final OAuth2Service oauth2Service;
    private final JwtService jwtService;
    
    @GetMapping("/providers")
    public Flux<OAuth2Provider> getProviders() {
        return oauth2Service.getEnabledProviders();
    }
    
    @GetMapping("/login/{providerName}")
    public Mono<ResponseEntity<Map<String, String>>> initiateLogin(
            @PathVariable String providerName,
            @RequestParam(required = false) String redirectUri) {
        String state = UUID.randomUUID().toString();
        return oauth2Service.generateAuthorizationUrl(providerName, state, redirectUri)
            .map(authUrl -> ResponseEntity.ok(Map.of("authorizationUrl", authUrl, "state", state)))
            .onErrorResume(e -> {
                log.error("Failed to initiate OAuth2 login", e);
                return Mono.just(ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to initiate OAuth2 login: " + e.getMessage())));
            });
    }
    
    @GetMapping("/callback/{providerName}")
    public Mono<ResponseEntity<Map<String, String>>> handleCallback(
            @PathVariable String providerName,
            @RequestParam String code,
            @RequestParam String state,
            @RequestParam(required = false) String redirectUri) {
        return oauth2Service.exchangeCodeForToken(providerName, code, redirectUri)
            .flatMap(tokenResponse -> {
                String accessToken = (String) tokenResponse.get("access_token");
                String refreshToken = (String) tokenResponse.get("refresh_token");
                return oauth2Service.getUserInfo(providerName, accessToken)
                    .flatMap(userInfo -> oauth2Service.linkOrCreateUser(providerName, userInfo, accessToken, refreshToken));
            })
            .flatMap(authUser -> {
                String jwtToken = jwtService.generateToken(authUser.getUsername(), authUser.getAuthUserId(),
                    java.util.Collections.emptyList(), java.util.Collections.emptyMap(), java.util.Collections.emptyList());
                return Mono.just(ResponseEntity.ok(Map.of(
                    "token", jwtToken,
                    "username", authUser.getUsername(),
                    "email", authUser.getEmail() != null ? authUser.getEmail() : ""
                )));
            })
            .onErrorResume(e -> {
                log.error("OAuth2 callback failed", e);
                return Mono.just(ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body(Map.of("error", "OAuth2 authentication failed: " + e.getMessage())));
            });
    }
}
"""

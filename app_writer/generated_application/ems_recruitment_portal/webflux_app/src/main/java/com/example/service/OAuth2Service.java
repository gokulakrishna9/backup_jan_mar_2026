package com.example.service;

import com.example.entity.OAuth2Provider;
import com.example.entity.OAuth2LinkedAccount;
import com.example.entity.AuthUser;
import com.example.repository.OAuth2ProviderRepository;
import com.example.repository.OAuth2LinkedAccountRepository;
import com.example.repository.AuthUserRepository;
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
package com.jobportal.controller;

import com.jobportal.service.OAuth2Service;
import com.jobportal.auth.JwtService;
import com.jobportal.entity.OAuth2Provider;
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
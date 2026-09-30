package com.jobportal.controller;

import com.jobportal.service.AuthService;
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
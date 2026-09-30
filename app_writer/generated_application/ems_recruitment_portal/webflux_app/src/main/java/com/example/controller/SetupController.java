package com.example.controller;

import com.example.service.SetupService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ServerWebExchange;
import reactor.core.publisher.Mono;
import lombok.RequiredArgsConstructor;

@Controller
@RequiredArgsConstructor
public class SetupController {
    
    private final SetupService setupService;
    
    @GetMapping("/setup")
    public Mono<String> showSetupForm(Model model, ServerWebExchange exchange) {
        return setupService.isSetupCompleted()
            .flatMap(completed -> {
                if (completed) {
                    return Mono.just("redirect:/login?message=Setup already completed");
                }
                model.addAttribute("setupRequest", new SetupRequest());
                return Mono.just("setup");
            });
    }
    
    @GetMapping("/login")
    public Mono<String> showLoginForm(Model model, ServerWebExchange exchange) {
        return setupService.isSetupCompleted()
            .flatMap(completed -> {
                if (!completed) {
                    return Mono.just("redirect:/setup");
                }
                return Mono.just("login");
            });
    }
    
    @PostMapping("/setup")
    public Mono<String> processSetup(@ModelAttribute SetupRequest request, Model model) {
        // Validate passwords match
        if (!request.getPassword().equals(request.getConfirmPassword())) {
            model.addAttribute("error", "Passwords do not match");
            model.addAttribute("setupRequest", request);
            return Mono.just("setup");
        }
        
        // Validate password strength (minimum 8 characters)
        if (request.getPassword().length() < 8) {
            model.addAttribute("error", "Password must be at least 8 characters");
            model.addAttribute("setupRequest", request);
            return Mono.just("setup");
        }
        
        return setupService.createSuperUser(
                request.getUsername(),
                request.getEmail(),
                request.getPassword()
            )
            .then(Mono.just("redirect:/login?message=Setup completed successfully. Please login."))
            .onErrorResume(e -> {
                model.addAttribute("error", e.getMessage());
                model.addAttribute("setupRequest", request);
                return Mono.just("setup");
            });
    }
    
    // DTO for setup form
    public static class SetupRequest {
        private String username;
        private String email;
        private String password;
        private String confirmPassword;
        
        public String getUsername() { return username; }
        public void setUsername(String username) { this.username = username; }
        
        public String getEmail() { return email; }
        public void setEmail(String email) { this.email = email; }
        
        public String getPassword() { return password; }
        public void setPassword(String password) { this.password = password; }
        
        public String getConfirmPassword() { return confirmPassword; }
        public void setConfirmPassword(String confirmPassword) { this.confirmPassword = confirmPassword; }
    }
}
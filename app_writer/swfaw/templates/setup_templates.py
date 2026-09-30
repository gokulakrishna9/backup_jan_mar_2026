"""Setup controller and service templates for initial super user creation."""


class SetupTemplates:
    """Templates for setup controller and related components."""
    
    # Setup Controller
    SETUP_CONTROLLER = """package {{ packageName }};

import {{ servicePackage }}.SetupService;
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
                    return Mono.just("redirect:/login?message=Setup+already+completed");
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
            .then(Mono.just("redirect:/login?message=Setup+completed+successfully.+Please+login."))
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
"""

    # Setup Service
    SETUP_SERVICE = """package {{ packageName }};

import {{ entityPackage }}.SystemConfig;
import {{ entityPackage }}.AuthUser;
import {{ entityPackage }}.UserRole;
import {{ repositoryPackage }}.SystemConfigRepository;
import {{ repositoryPackage }}.AuthUserRepository;
import {{ repositoryPackage }}.UserRoleRepository;
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
"""

    # Thymeleaf Setup Page
    THYMELEAF_SETUP_PAGE = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Initial Setup - Create Super User</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .setup-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 480px;
            width: 100%;
            padding: 40px;
        }
        
        .setup-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .setup-header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .setup-header p {
            color: #666;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .error-message {
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
        
        .submit-btn:active {
            transform: translateY(0);
        }
        
        .password-requirements {
            font-size: 12px;
            color: #666;
            margin-top: 6px;
        }
    </style>
</head>
<body>
    <div class="setup-container">
        <div class="setup-header">
            <h1>🚀 Initial Setup</h1>
            <p>Create your super administrator account</p>
        </div>
        
        <div th:if="${error}" class="error-message" th:text="${error}"></div>
        
        <form th:action="@{/setup}" th:object="${setupRequest}" method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" th:field="*{username}" required 
                       placeholder="Enter username" autocomplete="username">
            </div>
            
            <div class="form-group">
                <label for="email">Email Address</label>
                <input type="email" id="email" th:field="*{email}" required 
                       placeholder="Enter email address" autocomplete="email">
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" th:field="*{password}" required 
                       placeholder="Enter password" autocomplete="new-password">
                <div class="password-requirements">
                    Minimum 8 characters required
                </div>
            </div>
            
            <div class="form-group">
                <label for="confirmPassword">Confirm Password</label>
                <input type="password" id="confirmPassword" th:field="*{confirmPassword}" required 
                       placeholder="Confirm password" autocomplete="new-password">
            </div>
            
            <button type="submit" class="submit-btn">Create Super User</button>
        </form>
    </div>
</body>
</html>
"""

    # Thymeleaf Login Page
    THYMELEAF_LOGIN_PAGE = """<!DOCTYPE html>
<html xmlns:th="http://www.thymeleaf.org">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        
        .login-container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 420px;
            width: 100%;
            padding: 40px;
        }
        
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .login-header h1 {
            color: #333;
            font-size: 28px;
            margin-bottom: 10px;
        }
        
        .success-message {
            background: #efe;
            border: 1px solid #cfc;
            color: #3c3;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .error-message {
            background: #fee;
            border: 1px solid #fcc;
            color: #c33;
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            font-size: 14px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            color: #333;
            font-weight: 500;
            margin-bottom: 8px;
            font-size: 14px;
        }
        
        .form-group input {
            width: 100%;
            padding: 12px 16px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .submit-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Login</h1>
        </div>
        
        <div th:if="${param.message}" class="success-message" th:text="${param.message}"></div>
        <div th:if="${error}" class="error-message" th:text="${error}"></div>
        
        <form th:action="@{/api/auth/login}" method="post">
            <div class="form-group">
                <label for="username">Username</label>
                <input type="text" id="username" name="username" required 
                       placeholder="Enter username" autocomplete="username">
            </div>
            
            <div class="form-group">
                <label for="password">Password</label>
                <input type="password" id="password" name="password" required 
                       placeholder="Enter password" autocomplete="current-password">
            </div>
            
            <button type="submit" class="submit-btn">Login</button>
        </form>
    </div>
</body>
</html>
"""

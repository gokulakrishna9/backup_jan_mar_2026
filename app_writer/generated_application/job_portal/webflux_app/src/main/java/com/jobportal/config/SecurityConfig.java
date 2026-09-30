package com.jobportal.config;

import com.jobportal.security.JwtAuthenticationFilter;
import com.jobportal.exception.ErrorResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.buffer.DataBuffer;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.security.config.annotation.web.reactive.EnableWebFluxSecurity;
import org.springframework.security.config.web.server.SecurityWebFiltersOrder;
import org.springframework.security.config.web.server.ServerHttpSecurity;
import org.springframework.security.web.server.SecurityWebFilterChain;
import org.springframework.security.web.server.ServerAuthenticationEntryPoint;
import org.springframework.security.web.server.authorization.ServerAccessDeniedHandler;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.reactive.CorsConfigurationSource;
import org.springframework.web.cors.reactive.UrlBasedCorsConfigurationSource;
import com.jobportal.auth.JwtService;
import com.jobportal.service.AuthService;
import lombok.RequiredArgsConstructor;
import reactor.core.publisher.Mono;
import java.time.LocalDateTime;

@Configuration
@EnableWebFluxSecurity
@RequiredArgsConstructor
public class SecurityConfig {

    private final WebSecurityProperties securityProperties;
    private final ObjectMapper objectMapper;
    private final JwtService jwtService;
    private final AuthService authService;

    @Bean
    public JwtAuthenticationFilter jwtAuthenticationFilter() {
        return new JwtAuthenticationFilter(jwtService, authService, objectMapper);
    }

    @Bean
    public SecurityWebFilterChain securityWebFilterChain(ServerHttpSecurity http) {
        // Disable default form login
        http.formLogin(ServerHttpSecurity.FormLoginSpec::disable)
            .httpBasic(ServerHttpSecurity.HttpBasicSpec::disable);

        // CSRF - disabled by default, enable via app.security.csrf.enabled=true
        if (securityProperties.getCsrf().isEnabled()) {
            http.csrf(csrf -> csrf.csrfTokenRepository(
                org.springframework.security.web.server.csrf.WebSessionServerCsrfTokenRepository.class
                    .cast(new org.springframework.security.web.server.csrf.WebSessionServerCsrfTokenRepository())
            ));
        } else {
            http.csrf(ServerHttpSecurity.CsrfSpec::disable);
        }

        // CORS - disabled by default, enable via app.security.cors.enabled=true
        if (securityProperties.getCors().isEnabled()) {
            http.cors(cors -> cors.configurationSource(corsConfigurationSource()));
        } else {
            http.cors(ServerHttpSecurity.CorsSpec::disable);
        }

        // HTTPS redirect - disabled by default, enable via app.security.https.redirectHttp=true
        if (securityProperties.getHttps().isEnabled() && securityProperties.getHttps().isRedirectHttp()) {
            http.redirectToHttps(redirect -> redirect.httpsRedirectWhen(
                e -> e.getRequest().getHeaders().containsKey("X-Forwarded-Proto")
            ));
        }

        // Configure exception handling for 401 and 403 responses
        http.exceptionHandling(exceptionHandling -> exceptionHandling
            .authenticationEntryPoint(authenticationEntryPoint())
            .accessDeniedHandler(accessDeniedHandler())
        );

        // Public endpoints that don't require authentication
        http.authorizeExchange(exchanges -> exchanges
            .pathMatchers(
                "/api/auth/login", "/api/auth/register",
                "/setup/**", "/login/**",
                "/swagger-ui/**", "/swagger-ui.html", "/v3/api-docs/**",
                "/webjars/**", "/favicon.ico", "/"
            ).permitAll()
            .anyExchange().authenticated()
        );

        // Add JWT filter (bean-managed, not auto-registered as global WebFilter)
        http.addFilterAt(jwtAuthenticationFilter(), SecurityWebFiltersOrder.AUTHENTICATION);

        // Authorization is handled by AuthorizationAspect (AOP) — no WebFilter needed

        return http.build();
    }

    /**
     * Handles 401 Unauthorized - when no valid authentication is present.
     */
    private ServerAuthenticationEntryPoint authenticationEntryPoint() {
        return (exchange, ex) -> {
            var response = exchange.getResponse();
            response.setStatusCode(HttpStatus.UNAUTHORIZED);
            response.getHeaders().setContentType(MediaType.APPLICATION_JSON);

            ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.UNAUTHORIZED.value())
                .error(HttpStatus.UNAUTHORIZED.getReasonPhrase())
                .message("Authentication required. Please provide a valid JWT token.")
                .path(exchange.getRequest().getPath().value())
                .errorCode("AUTHENTICATION_REQUIRED")
                .build();

            try {
                byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
                DataBuffer buffer = response.bufferFactory().wrap(bytes);
                return response.writeWith(Mono.just(buffer));
            } catch (Exception e) {
                return response.setComplete();
            }
        };
    }

    /**
     * Handles 403 Forbidden - when authenticated but insufficient permissions.
     */
    private ServerAccessDeniedHandler accessDeniedHandler() {
        return (exchange, denied) -> {
            var response = exchange.getResponse();
            response.setStatusCode(HttpStatus.FORBIDDEN);
            response.getHeaders().setContentType(MediaType.APPLICATION_JSON);

            ErrorResponse errorResponse = ErrorResponse.builder()
                .timestamp(LocalDateTime.now())
                .status(HttpStatus.FORBIDDEN.value())
                .error(HttpStatus.FORBIDDEN.getReasonPhrase())
                .message("Access denied. You do not have permission to access this resource.")
                .path(exchange.getRequest().getPath().value())
                .errorCode("ACCESS_DENIED")
                .build();

            try {
                byte[] bytes = objectMapper.writeValueAsBytes(errorResponse);
                DataBuffer buffer = response.bufferFactory().wrap(bytes);
                return response.writeWith(Mono.just(buffer));
            } catch (Exception e) {
                return response.setComplete();
            }
        };
    }

    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        WebSecurityProperties.Cors corsProps = securityProperties.getCors();
        config.setAllowedOrigins(corsProps.getAllowedOrigins());
        config.setAllowedMethods(corsProps.getAllowedMethods());
        config.setAllowedHeaders(corsProps.getAllowedHeaders());
        config.setAllowCredentials(corsProps.isAllowCredentials());
        config.setMaxAge(corsProps.getMaxAge());

        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
"""Configuration templates for code generation."""


class ConfigTemplates:
    """Templates for application configuration generation."""
    
    APPLICATION_YML_TEMPLATE = """spring:
  application:
    name: {{ projectName }}
  r2dbc:
    url: r2dbc:{{ databaseType }}://{{ databaseHost }}:{{ databasePort }}/{{ databaseName }}
    username: ${DB_USERNAME:root}
    password: ${DB_PASSWORD:password}
  data:
    r2dbc:
      repositories:
        enabled: true

server:
  port: {{ port }}

jwt:
  secret: ${JWT_SECRET:your-secret-key-change-in-production}
  expiration: 86400000

# Security settings - all features disabled by default
# Uncomment and configure as needed
app:
  security:
    csrf:
      enabled: false
    cors:
      enabled: true
      allowed-origins:
        - "http://localhost:5173"
        - "http://localhost:{{ port }}"
        - "null"
      allowed-methods:
        - GET
        - POST
        - PUT
        - DELETE
        - OPTIONS
      allowed-headers:
        - "*"
      allow-credentials: true
      max-age: 3600
    https:
      enabled: false
      redirect-http: false
      https-port: 8443

logging:
  level:
    root: INFO
    {{ packageName }}: DEBUG
"""
    
    DATABASE_CONFIG_TEMPLATE = """package {{ packageName }};

import org.springframework.context.annotation.Configuration;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;

/**
 * R2DBC configuration.
 * Connection factory is auto-configured from application.yml
 */
@Configuration
@EnableR2dbcRepositories
public class DatabaseConfig {
    // R2DBC auto-configuration handles connection factory
}
"""
    
    SWAGGER_CONFIG_TEMPLATE = """package {{ packageName }};

import io.swagger.v3.oas.models.OpenAPI;
import io.swagger.v3.oas.models.info.Info;
import io.swagger.v3.oas.models.security.SecurityRequirement;
import io.swagger.v3.oas.models.security.SecurityScheme;
import io.swagger.v3.oas.models.Components;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class SwaggerConfig {
    
    private static final String SECURITY_SCHEME_NAME = "bearerAuth";

    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("{{ projectName }} API")
                .version("1.0.0")
                .description("API documentation for {{ projectName }}"))
            .addSecurityItem(new SecurityRequirement().addList(SECURITY_SCHEME_NAME))
            .components(new Components()
                .addSecuritySchemes(SECURITY_SCHEME_NAME, new SecurityScheme()
                    .name(SECURITY_SCHEME_NAME)
                    .type(SecurityScheme.Type.HTTP)
                    .scheme("bearer")
                    .bearerFormat("JWT")
                    .description("Enter JWT token obtained from /api/auth/login")));
    }
}
"""
    
    MAIN_APPLICATION_TEMPLATE = """package {{ packageName }};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.data.r2dbc.repository.config.EnableR2dbcRepositories;

@SpringBootApplication
@EnableR2dbcRepositories
@EnableConfigurationProperties
public class Application {

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}
"""

package com.jobportal.config;

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
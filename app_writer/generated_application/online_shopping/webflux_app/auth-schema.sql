-- ============================================================================
-- Authentication and Authorization Schema
-- ============================================================================
-- This schema must be run manually against your database before starting
-- the application for the first time.
--
-- Simplified role-based authorization model:
--   3 roles: USER, TABLE_ADMIN, SUPER_ADMIN
--   Record ownership tracking via record_owner table
--   Query groups for sharing records across users
-- ============================================================================

-- System configuration table
CREATE TABLE IF NOT EXISTS system_config (
    config_key VARCHAR(255) PRIMARY KEY,
    config_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default setup flag
INSERT INTO system_config (config_key, config_value) 
VALUES ('setup_completed', 'false')
ON DUPLICATE KEY UPDATE config_key=config_key;

-- ============================================================================
-- Authentication Tables
-- ============================================================================

-- Auth users (separate from business users)
CREATE TABLE IF NOT EXISTS auth_user (
    auth_user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Role-Based Authorization Tables
-- ============================================================================

-- User roles (USER, TABLE_ADMIN, SUPER_ADMIN)
CREATE TABLE IF NOT EXISTS user_role (
    user_role_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    role ENUM('USER', 'TABLE_ADMIN', 'SUPER_ADMIN') NOT NULL,
    table_name VARCHAR(255) NULL,
    granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    granted_by_auth_user_id BIGINT UNSIGNED NULL,
    INDEX idx_auth_user (auth_user_id),
    INDEX idx_role (role),
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE,
    FOREIGN KEY (granted_by_auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Record ownership tracking
CREATE TABLE IF NOT EXISTS record_owner (
    record_owner_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    record_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_auth_user (auth_user_id),
    INDEX idx_table_record (table_name, record_id),
    UNIQUE KEY unique_table_record (table_name, record_id),
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Query Group Tables
-- ============================================================================

-- Query groups (SYSTEM or COMMUNITY)
CREATE TABLE IF NOT EXISTS query_group (
    query_group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    group_name VARCHAR(255) UNIQUE NOT NULL,
    group_type ENUM('SYSTEM', 'COMMUNITY') NOT NULL,
    owner_auth_user_id BIGINT UNSIGNED NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_group_type (group_type),
    INDEX idx_owner (owner_auth_user_id),
    FOREIGN KEY (owner_auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Queries belonging to a query group
CREATE TABLE IF NOT EXISTS query_group_query (
    query_group_query_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    query_group_id BIGINT UNSIGNED NOT NULL,
    query_name VARCHAR(255) NOT NULL,
    UNIQUE KEY unique_group_query (query_group_id, query_name),
    FOREIGN KEY (query_group_id) REFERENCES query_group(query_group_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Query group members
CREATE TABLE IF NOT EXISTS query_group_member (
    query_group_member_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    query_group_id BIGINT UNSIGNED NOT NULL,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    invited_by_auth_user_id BIGINT UNSIGNED NULL,
    UNIQUE KEY unique_group_member (query_group_id, auth_user_id),
    FOREIGN KEY (query_group_id) REFERENCES query_group(query_group_id) ON DELETE CASCADE,
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE,
    FOREIGN KEY (invited_by_auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Records shared via query groups
CREATE TABLE IF NOT EXISTS query_group_record (
    query_group_record_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    query_group_id BIGINT UNSIGNED NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    record_id BIGINT UNSIGNED NOT NULL,
    added_by_auth_user_id BIGINT UNSIGNED NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_group_table_record (query_group_id, table_name, record_id),
    FOREIGN KEY (query_group_id) REFERENCES query_group(query_group_id) ON DELETE CASCADE,
    FOREIGN KEY (added_by_auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- Audit Logging Tables
-- ============================================================================

-- Access audit log
CREATE TABLE IF NOT EXISTS access_audit_log (
    audit_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    action VARCHAR(50) NOT NULL,
    table_name VARCHAR(255) NOT NULL,
    record_id BIGINT UNSIGNED,
    access_granted BOOLEAN NOT NULL,
    denial_reason TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_time (auth_user_id, accessed_at),
    INDEX idx_table_record (table_name, record_id),
    INDEX idx_action (action),
    INDEX idx_granted (access_granted),
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- OAuth2 / OpenID Connect Tables
-- ============================================================================

-- OAuth2 providers configuration
CREATE TABLE IF NOT EXISTS oauth2_provider (
    provider_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    provider_name VARCHAR(50) UNIQUE NOT NULL, -- google, github, microsoft, facebook, custom
    display_name VARCHAR(100) NOT NULL,
    client_id VARCHAR(255) NOT NULL,
    client_secret VARCHAR(255) NOT NULL,
    authorization_uri VARCHAR(500),
    token_uri VARCHAR(500),
    user_info_uri VARCHAR(500),
    jwk_set_uri VARCHAR(500),
    issuer_uri VARCHAR(500),
    scope VARCHAR(255) DEFAULT 'openid profile email',
    is_enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_provider_name (provider_name),
    INDEX idx_enabled (is_enabled)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- OAuth2 linked accounts (external identities linked to local users)
CREATE TABLE IF NOT EXISTS oauth2_linked_account (
    linked_account_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    auth_user_id BIGINT UNSIGNED NOT NULL,
    provider_id BIGINT UNSIGNED NOT NULL,
    provider_user_id VARCHAR(255) NOT NULL, -- External user ID from provider
    provider_username VARCHAR(255),
    provider_email VARCHAR(255),
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMP NULL,
    linked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login_at TIMESTAMP NULL,
    INDEX idx_user (auth_user_id),
    INDEX idx_provider (provider_id),
    INDEX idx_provider_user (provider_id, provider_user_id),
    UNIQUE KEY unique_provider_account (provider_id, provider_user_id),
    FOREIGN KEY (auth_user_id) REFERENCES auth_user(auth_user_id) ON DELETE CASCADE,
    FOREIGN KEY (provider_id) REFERENCES oauth2_provider(provider_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- ============================================================================
-- Schema Setup Complete
-- ============================================================================

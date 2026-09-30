CREATE DATABASE IF NOT EXISTS `online_shopping`;
USE `online_shopping`;

CREATE TABLE IF NOT EXISTS `user` (
    `user_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(255),
    `encrypted_password` VARCHAR(255),
    `email` VARCHAR(255),
    `first_name` VARCHAR(255),
    `last_name` VARCHAR(255),
    `phone` VARCHAR(255),
    `role` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `category` (
    `category_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `category_name` VARCHAR(255),
    `description` VARCHAR(255),
    `image_url` VARCHAR(255),
    `parent_category_id` BIGINT UNSIGNED,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `product` (
    `product_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `product_name` VARCHAR(255),
    `description` VARCHAR(255),
    `price` DECIMAL(19,4),
    `stock_quantity` INT,
    `image_url` VARCHAR(255),
    `sku` VARCHAR(255),
    `is_active` BOOLEAN,
    `category_id` BIGINT UNSIGNED,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `cart` (
    `cart_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED,
    `total_amount` DECIMAL(19,4),
    `item_count` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`cart_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `cart_item` (
    `cart_item_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `cart_id` BIGINT UNSIGNED,
    `product_id` BIGINT UNSIGNED,
    `quantity` INT,
    `unit_price` DECIMAL(19,4),
    `subtotal` DECIMAL(19,4),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`cart_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `address` (
    `address_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED,
    `address_line1` VARCHAR(255),
    `address_line2` VARCHAR(255),
    `city` VARCHAR(255),
    `state` VARCHAR(255),
    `postal_code` VARCHAR(255),
    `country` VARCHAR(255),
    `is_default` BOOLEAN,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`address_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `order` (
    `order_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED,
    `order_date` TIMESTAMP,
    `status` VARCHAR(255),
    `total_amount` DECIMAL(19,4),
    `shipping_address_id` BIGINT UNSIGNED,
    `tracking_number` VARCHAR(255),
    `notes` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `order_item` (
    `order_item_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` BIGINT UNSIGNED,
    `product_id` BIGINT UNSIGNED,
    `quantity` INT,
    `unit_price` DECIMAL(19,4),
    `subtotal` DECIMAL(19,4),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`order_item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `payment` (
    `payment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `order_id` BIGINT UNSIGNED,
    `payment_method` VARCHAR(255),
    `amount` DECIMAL(19,4),
    `payment_date` TIMESTAMP,
    `transaction_id` VARCHAR(255),
    `status` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `review` (
    `review_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `user_id` BIGINT UNSIGNED,
    `product_id` BIGINT UNSIGNED,
    `rating` INT,
    `title` VARCHAR(255),
    `comment` VARCHAR(255),
    `review_date` TIMESTAMP,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

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


-- Activity Tracking Schema
-- Tables for tracking user activities: CRUD operations, logins, and grants

-- Table: crud_activity_log
-- Tracks all CRUD operations on entities
CREATE TABLE IF NOT EXISTS crud_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    username VARCHAR(255),
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT,
    operation VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    changes_json TEXT,
    success BOOLEAN DEFAULT TRUE,
    error_message TEXT,
    INDEX idx_user_id (user_id),
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_operation (operation),
    INDEX idx_timestamp (timestamp)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: deleted_record
-- Stores complete deleted records as JSON for recovery
CREATE TABLE IF NOT EXISTS deleted_record (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    entity_type VARCHAR(100) NOT NULL,
    entity_id BIGINT NOT NULL,
    record_json LONGTEXT NOT NULL,
    deleted_by_user_id BIGINT,
    deleted_by_username VARCHAR(255),
    deleted_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    reason TEXT,
    can_restore BOOLEAN DEFAULT TRUE,
    INDEX idx_entity (entity_type, entity_id),
    INDEX idx_deleted_by (deleted_by_user_id),
    INDEX idx_deleted_at (deleted_at),
    INDEX idx_can_restore (can_restore)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: login_activity_log
-- Tracks login and logout events
CREATE TABLE IF NOT EXISTS login_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT,
    username VARCHAR(255),
    activity_type VARCHAR(20) NOT NULL,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    session_id VARCHAR(255),
    success BOOLEAN DEFAULT TRUE,
    failure_reason TEXT,
    login_method VARCHAR(50),
    oauth2_provider VARCHAR(50),
    INDEX idx_user_id (user_id),
    INDEX idx_username (username),
    INDEX idx_activity_type (activity_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_success (success)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: grant_activity_log
-- Tracks permission and grant changes
CREATE TABLE IF NOT EXISTS grant_activity_log (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    granted_by_user_id BIGINT,
    granted_by_username VARCHAR(255),
    target_user_id BIGINT,
    target_username VARCHAR(255),
    grant_type VARCHAR(50) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_type VARCHAR(100),
    entity_id BIGINT,
    previous_value_json TEXT,
    new_value_json TEXT,
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    reason TEXT,
    INDEX idx_granted_by (granted_by_user_id),
    INDEX idx_target_user (target_user_id),
    INDEX idx_grant_type (grant_type),
    INDEX idx_timestamp (timestamp),
    INDEX idx_entity (entity_type, entity_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

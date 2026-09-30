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

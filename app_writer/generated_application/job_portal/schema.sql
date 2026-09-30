CREATE DATABASE IF NOT EXISTS `job_portal`;
USE `job_portal`;

CREATE TABLE IF NOT EXISTS `student_profile` (
    `student_profile_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `resume_url` VARCHAR(255),
    `skills` VARCHAR(255),
    `education_level` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`student_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `employer_profile` (
    `employer_profile_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `company_name` VARCHAR(255),
    `industry` VARCHAR(255),
    `website` VARCHAR(255),
    `logo_url` VARCHAR(255),
    `description` VARCHAR(255),
    `contact_email` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`employer_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `trainer_profile` (
    `trainer_profile_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `specialization` VARCHAR(255),
    `certifications` VARCHAR(255),
    `hourly_rate` DECIMAL(19,4),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`trainer_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_posting` (
    `job_posting_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `location` VARCHAR(255),
    `salary_min` DECIMAL(19,4),
    `salary_max` DECIMAL(19,4),
    `job_type` VARCHAR(255),
    `is_active` BOOLEAN,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`job_posting_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `training_program` (
    `training_program_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `duration_days` INT,
    `price` DECIMAL(19,4),
    `is_active` BOOLEAN,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`training_program_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_application` (
    `job_application_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `status` VARCHAR(255),
    `cover_letter` VARCHAR(255),
    `applied_at` TIMESTAMP,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`job_application_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `training_enrollment` (
    `training_enrollment_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `status` VARCHAR(255),
    `progress` INT,
    `enrolled_at` TIMESTAMP,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`training_enrollment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_profile` (
    `user_profile_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(255),
    `last_name` VARCHAR(255),
    `email` VARCHAR(255),
    `phone` VARCHAR(255),
    `bio` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_profile_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `education_level` (
    `education_level_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`education_level_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `field_of_study` (
    `field_of_study_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`field_of_study_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `institution` (
    `institution_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `country` VARCHAR(255),
    `website` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`institution_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_education` (
    `user_education_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `institution_name` VARCHAR(255),
    `degree` VARCHAR(255),
    `field_of_study` VARCHAR(255),
    `start_date` DATE,
    `end_date` DATE,
    `grade` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_education_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `industry` (
    `industry_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`industry_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `job_title` (
    `job_title_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`job_title_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_work_experience` (
    `user_work_experience_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `company_name` VARCHAR(255),
    `job_title` VARCHAR(255),
    `industry` VARCHAR(255),
    `location` VARCHAR(255),
    `start_date` DATE,
    `end_date` DATE,
    `is_current` BOOLEAN,
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_work_experience_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `skill_category` (
    `skill_category_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`skill_category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `skill` (
    `skill_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `category` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `user_skill` (
    `user_skill_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `skill_name` VARCHAR(255),
    `proficiency_level` VARCHAR(255),
    `years_of_experience` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`user_skill_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `training_module` (
    `training_module_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `module_order` INT,
    `duration_minutes` INT,
    `content_url` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`training_module_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `module_progress` (
    `module_progress_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `status` VARCHAR(255),
    `completed_at` TIMESTAMP,
    `progress_percent` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`module_progress_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `training_exam` (
    `training_exam_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `passing_score` INT,
    `max_score` INT,
    `time_limit_minutes` INT,
    `max_attempts` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`training_exam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `exam_attempt` (
    `exam_attempt_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `score` INT,
    `passed` BOOLEAN,
    `started_at` TIMESTAMP,
    `completed_at` TIMESTAMP,
    `attempt_number` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`exam_attempt_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `training_certification` (
    `training_certification_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `certificate_number` VARCHAR(255),
    `title` VARCHAR(255),
    `issued_at` TIMESTAMP,
    `expires_at` TIMESTAMP,
    `certificate_url` VARCHAR(255),
    `status` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`training_certification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_document` (
    `course_document_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `content` VARCHAR(255),
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_document_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_video` (
    `course_video_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `video_url` VARCHAR(255),
    `duration_seconds` INT,
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_video_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_audio` (
    `course_audio_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `audio_url` VARCHAR(255),
    `duration_seconds` INT,
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_audio_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_code_lab` (
    `course_code_lab_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255),
    `description` VARCHAR(255),
    `language` VARCHAR(255),
    `starter_code` VARCHAR(255),
    `solution_code` VARCHAR(255),
    `instructions` VARCHAR(255),
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_code_lab_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `exam_question` (
    `exam_question_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `question_text` VARCHAR(255),
    `question_code` VARCHAR(255),
    `question_type` VARCHAR(255),
    `points` INT,
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`exam_question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `exam_answer` (
    `exam_answer_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `answer_text` VARCHAR(255),
    `answer_code` VARCHAR(255),
    `is_correct` BOOLEAN,
    `explanation` VARCHAR(255),
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`exam_answer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_question` (
    `course_question_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `question_text` VARCHAR(255),
    `question_code` VARCHAR(255),
    `sort_order` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_question_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `course_answer` (
    `course_answer_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `answer_text` VARCHAR(255),
    `answer_code` VARCHAR(255),
    `is_accepted` BOOLEAN,
    `upvotes` INT,
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`course_answer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `company` (
    `company_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255),
    `industry` VARCHAR(255),
    `website` VARCHAR(255),
    `description` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`company_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `location` (
    `location_id` BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    `city` VARCHAR(255),
    `state` VARCHAR(255),
    `country` VARCHAR(255),
    `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`location_id`)
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

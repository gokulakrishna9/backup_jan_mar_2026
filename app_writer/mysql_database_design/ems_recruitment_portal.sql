-- Database: ems_recruitment_portal
-- Generated: 2026-02-02
-- Purpose: Schema for Job & Training portal (users, institutions, courses, jobs, communities, AI evaluations, payments, properties, links, posts)

SET FOREIGN_KEY_CHECKS = 0;

CREATE DATABASE IF NOT EXISTS `ems_recruitment_portal` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ems_recruitment_portal`;

-- 1) Users
CREATE TABLE IF NOT EXISTS ems_user (
  user_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  gender ENUM('male','female','other') DEFAULT 'other',
  date_of_birth DATE NULL,
  email_address VARCHAR(255) NOT NULL UNIQUE,
  user_name VARCHAR(100) NOT NULL UNIQUE,
  encrypted_password VARCHAR(255) NOT NULL,
  phone_number VARCHAR(30) NULL,
  profile_photo VARCHAR(255) NULL,
  is_active TINYINT(1) DEFAULT 1,
  is_entity TINYINT(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 2) User property groups and properties
CREATE TABLE IF NOT EXISTS ems_user_property_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  user_id BIGINT UNSIGNED NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (user_id),
  CONSTRAINT fk_user_property_group_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_property (
  property_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  property_name VARCHAR(150) NOT NULL,
  property_value TEXT NULL,
  property_type VARCHAR(50) NOT NULL,
  property_description TEXT NULL,
  group_id BIGINT UNSIGNED NULL,
  user_id BIGINT UNSIGNED NULL,
  INDEX (group_id),
  INDEX (user_id),
  CONSTRAINT fk_user_property_group FOREIGN KEY (group_id) REFERENCES ems_user_property_group(group_id) ON DELETE SET NULL,
  CONSTRAINT fk_user_property_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3) Institutions
CREATE TABLE IF NOT EXISTS ems_institution (
  institution_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  moto VARCHAR(255) NULL,
  institution_type_id INT NULL,
  website VARCHAR(255) NULL,
  contact_email VARCHAR(255) NULL,
  contact_phone VARCHAR(30) NULL,
  is_active TINYINT(1) DEFAULT 1,
  is_entity TINYINT(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_institution_property_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  institution_id BIGINT UNSIGNED NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (institution_id),
  CONSTRAINT fk_inst_prop_group_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_institution_property (
  property_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  property_name VARCHAR(150) NOT NULL,
  property_value TEXT NULL,
  property_type VARCHAR(50) NOT NULL,
  property_description TEXT NULL,
  group_id BIGINT UNSIGNED NULL,
  institution_id BIGINT UNSIGNED NOT NULL,
  INDEX (group_id),
  INDEX (institution_id),
  CONSTRAINT fk_inst_property_group FOREIGN KEY (group_id) REFERENCES ems_institution_property_group(group_id) ON DELETE SET NULL,
  CONSTRAINT fk_inst_property_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Candidate/Institute links and user-institute property links
CREATE TABLE IF NOT EXISTS ems_candidate_institute_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  institution_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,
  status VARCHAR(50) DEFAULT 'requested', -- requested, accepted, rejected  INDEX (user_id),
  INDEX (institution_id),
  CONSTRAINT fk_candidate_institute_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_candidate_institute_inst FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_institute_property_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  property_id BIGINT UNSIGNED NOT NULL, -- refers to ems_institution_property.property_id
  comment TEXT NULL,
  INDEX (user_id),
  INDEX (property_id),
  CONSTRAINT fk_user_institute_prop_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_institute_prop_link_property FOREIGN KEY (property_id) REFERENCES ems_institution_property(property_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Courses and course properties
CREATE TABLE IF NOT EXISTS ems_course (
  course_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  outcomes TEXT NULL,
  course_type_id INT NULL,
  is_published TINYINT(1) DEFAULT 0,
  price DECIMAL(10,2) DEFAULT 0.00,
  duration_weeks INT NULL,
  institution_id BIGINT UNSIGNED NULL,
  is_entity TINYINT(1) DEFAULT 0,
  INDEX (institution_id),
  CONSTRAINT fk_course_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_course_property_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (course_id),
  CONSTRAINT fk_course_prop_group_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_course_property (
  property_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  property_name VARCHAR(150) NOT NULL,
  property_value TEXT NULL,
  property_type VARCHAR(50) NOT NULL,
  property_description TEXT NULL,
  group_id BIGINT UNSIGNED NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  INDEX (group_id),
  INDEX (course_id),
  CONSTRAINT fk_course_property_group FOREIGN KEY (group_id) REFERENCES ems_course_property_group(group_id) ON DELETE SET NULL,
  CONSTRAINT fk_course_property_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_course_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  role VARCHAR(50) DEFAULT 'enrolled', -- enrolled, instructor, completed  INDEX (user_id),
  INDEX (course_id),
  CONSTRAINT fk_user_course_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_course_link_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_course_wishlist (
  wish_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,  INDEX (user_id),
  INDEX (course_id),
  CONSTRAINT fk_wishlist_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_wishlist_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_course_purchase (
  purchase_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,
  amount DECIMAL(10,2) NOT NULL DEFAULT 0.00,
  transaction_id VARCHAR(255) NULL,
  purchased_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (user_id),
  INDEX (course_id),
  CONSTRAINT fk_purchase_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_purchase_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job posts and properties
CREATE TABLE IF NOT EXISTS ems_job_post (
  job_post_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_subject VARCHAR(255) NOT NULL,
  job_post_description TEXT NULL,
  institution_id BIGINT UNSIGNED NULL,
  location VARCHAR(255) NULL,
  salary_range VARCHAR(100) NULL,
  posted_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_on TIMESTAMP NULL,
  is_active TINYINT(1) DEFAULT 1,
  is_entity TINYINT(1) DEFAULT 0,
  INDEX (institution_id),
  CONSTRAINT fk_job_post_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_job_post_property_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  job_post_id BIGINT UNSIGNED NOT NULL,
  INDEX (job_post_id),
  CONSTRAINT fk_job_post_prop_group_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_job_post_property (
  property_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  property_name VARCHAR(150) NOT NULL,
  property_value TEXT NULL,
  property_type VARCHAR(50) NOT NULL,
  property_description TEXT NULL,
  group_id BIGINT UNSIGNED NULL,
  job_post_id BIGINT UNSIGNED NOT NULL,
  INDEX (group_id),
  INDEX (job_post_id),
  CONSTRAINT fk_job_post_property_group FOREIGN KEY (group_id) REFERENCES ems_job_post_property_group(group_id) ON DELETE SET NULL,
  CONSTRAINT fk_job_post_property_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_user_job_post_bookmark (
  bookmark_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  job_post_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,
  INDEX (user_id),
  INDEX (job_post_id),
  CONSTRAINT fk_user_job_bookmark_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_job_bookmark_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Note: ems_job_post_user_bookmark appears redundant with ems_user_job_post_bookmark, but included for compatibility
CREATE TABLE IF NOT EXISTS ems_job_post_user_bookmark (
  bookmark_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,
  INDEX (job_post_id),
  INDEX (user_id),
  CONSTRAINT fk_job_post_user_bookmark_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE,
  CONSTRAINT fk_job_post_user_bookmark_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Subscription payment history
CREATE TABLE IF NOT EXISTS ems_subscription_payment_history (
  payment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  amount DECIMAL(12,2) NOT NULL DEFAULT 0.00,
  subscription_type VARCHAR(100) NULL,
  transaction_details JSON NULL,
  transaction_reference VARCHAR(255) NULL,
  payment_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (user_id),
  CONSTRAINT fk_subscription_payment_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Communities
CREATE TABLE IF NOT EXISTS ems_community (
  community_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institute_id BIGINT UNSIGNED NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  group_owner_user_id BIGINT UNSIGNED NULL,
  is_entity TINYINT(1) DEFAULT 1,
  INDEX (institute_id),
  INDEX (group_owner_user_id),
  CONSTRAINT fk_community_institution FOREIGN KEY (institute_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL,
  CONSTRAINT fk_community_owner FOREIGN KEY (group_owner_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_community_property_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  community_id BIGINT UNSIGNED NOT NULL,
  INDEX (community_id),
  CONSTRAINT fk_community_prop_group_comm FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_community_property (
  property_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  property_name VARCHAR(150) NOT NULL,
  property_value TEXT NULL,
  property_type VARCHAR(50) NOT NULL,
  property_description TEXT NULL,
  group_id BIGINT UNSIGNED NULL,
  community_id BIGINT UNSIGNED NOT NULL,
  INDEX (group_id),
  INDEX (community_id),
  CONSTRAINT fk_community_property_group FOREIGN KEY (group_id) REFERENCES ems_community_property_group(group_id) ON DELETE SET NULL,
  CONSTRAINT fk_community_property_comm FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_community_user_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  role VARCHAR(50) DEFAULT 'member', -- member, moderator, owner
  comment TEXT NULL,  INDEX (community_id),
  INDEX (user_id),
  CONSTRAINT fk_community_user_link_comm FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_user_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_community_property_user_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_property_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NULL,  INDEX (community_property_id),
  INDEX (user_id),
  CONSTRAINT fk_community_prop_user_link_property FOREIGN KEY (community_property_id) REFERENCES ems_community_property(property_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_prop_user_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Posts within communities
CREATE TABLE IF NOT EXISTS ems_community_user_post (
  post_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  post JSON NOT NULL,  is_pinned TINYINT(1) DEFAULT 0,
  INDEX (community_id),
  INDEX (user_id),
  CONSTRAINT fk_community_post_comm FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_post_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_community_post_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  post_id BIGINT UNSIGNED NOT NULL,
  community_id BIGINT UNSIGNED NOT NULL,  INDEX (post_id),
  INDEX (community_id),
  CONSTRAINT fk_community_post_link_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_post_link_comm FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Emogi (emoji) and links
CREATE TABLE IF NOT EXISTS ems_post_emogi (
  emogi_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150) NOT NULL,
  description TEXT NULL,
  file_location VARCHAR(255) NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_emogi_post_user_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  emogi_id BIGINT UNSIGNED NOT NULL,
  post_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  INDEX (emogi_id),
  INDEX (post_id),
  INDEX (user_id),
  CONSTRAINT fk_emogi_post_link_emogi FOREIGN KEY (emogi_id) REFERENCES ems_post_emogi(emogi_id) ON DELETE CASCADE,
  CONSTRAINT fk_emogi_post_link_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE,
  CONSTRAINT fk_emogi_post_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_post_flag (
  flag_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  type VARCHAR(100) NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  post_id BIGINT UNSIGNED NOT NULL,
  reason TEXT NULL,
  flagged_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  INDEX (user_id),
  INDEX (post_id),
  CONSTRAINT fk_post_flag_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_post_flag_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_post_comment (
  comment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  post_id BIGINT UNSIGNED NOT NULL,
  comment TEXT NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  INDEX (post_id),
  INDEX (user_id),
  CONSTRAINT fk_post_comment_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE,
  CONSTRAINT fk_post_comment_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_post_comment_emogi_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  comment_id BIGINT UNSIGNED NOT NULL,
  emogi_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  INDEX (comment_id),
  INDEX (emogi_id),
  INDEX (user_id),
  CONSTRAINT fk_comment_emogi_link_comment FOREIGN KEY (comment_id) REFERENCES ems_post_comment(comment_id) ON DELETE CASCADE,
  CONSTRAINT fk_comment_emogi_link_emogi FOREIGN KEY (emogi_id) REFERENCES ems_post_emogi(emogi_id) ON DELETE CASCADE,
  CONSTRAINT fk_comment_emogi_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- AI Evaluations and parameter groups
CREATE TABLE IF NOT EXISTS ems_ai_user_profile_evaluation_parameter_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  description TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_user_profile_evaluation_parameter (
  parameter_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parameter_name VARCHAR(150) NOT NULL,
  group_id BIGINT UNSIGNED NOT NULL,
  parameter_value JSON NULL,
  INDEX (group_id),
  CONSTRAINT fk_ai_user_param_group FOREIGN KEY (group_id) REFERENCES ems_ai_user_profile_evaluation_parameter_group(group_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_user_profile_evaluation (
  evaluation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  property_id BIGINT UNSIGNED NULL, -- reference to ems_user_property.property_id
  evaluation_summary JSON NULL,
  rating DECIMAL(3,2) NULL,
  INDEX (user_id),
  INDEX (property_id),
  CONSTRAINT fk_ai_user_eval_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_ai_user_eval_property FOREIGN KEY (property_id) REFERENCES ems_user_property(property_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_evaluation_parameter_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  description TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_evaluation_parameter (
  parameter_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parameter_name VARCHAR(150) NOT NULL,
  parameter_group_id BIGINT UNSIGNED NOT NULL,
  parameter_value JSON NULL,
  INDEX (parameter_group_id),
  CONSTRAINT fk_ai_eval_param_group FOREIGN KEY (parameter_group_id) REFERENCES ems_ai_evaluation_parameter_group(group_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_institution_profile_evaluation (
  evaluation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  evaluation_summary JSON NULL,
  rating DECIMAL(3,2) NULL,
  INDEX (institution_id),
  CONSTRAINT fk_ai_inst_eval_inst FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_job_recommendation (
  preference_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  profile_id BIGINT UNSIGNED NOT NULL, -- user profile id
  preference_rating DECIMAL(3,2) NULL,
  recommendation_summary JSON NULL,
  INDEX (job_post_id),
  INDEX (profile_id),
  CONSTRAINT fk_ai_reco_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_community_post_evaluation (
  evaluation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  post_id BIGINT UNSIGNED NOT NULL,
  evaluation_summary JSON NULL,
  rating DECIMAL(3,2) NULL,
  INDEX (post_id),
  CONSTRAINT fk_ai_comm_post_eval_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_market_trend_parameter_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  description TEXT NULL,
  trend_id BIGINT UNSIGNED NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_market_trend_parameter (
  parameter_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  parameter_name VARCHAR(150) NOT NULL,
  parameter_value JSON NULL,
  group_id BIGINT UNSIGNED NULL,
  INDEX (group_id),
  CONSTRAINT fk_market_param_group FOREIGN KEY (group_id) REFERENCES ems_ai_market_trend_parameter_group(group_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_ai_market_trend_property (
  trend_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_name VARCHAR(255) NOT NULL,
  trend_description TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Misc: indexes and helper views can be added as needed

-- Document tables: user_profile, institution_profile, course document group & course documents, market_trend

CREATE TABLE IF NOT EXISTS ems_user_profile_document (
  document_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NULL,
  document JSON NOT NULL,
  document_type VARCHAR(100) NULL,
  INDEX (user_id),
  CONSTRAINT fk_user_profile_document_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_institution_profile_document (
  document_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NULL,
  document JSON NOT NULL,
  document_type VARCHAR(100) NULL,
  INDEX (institution_id),
  CONSTRAINT fk_institution_profile_document_inst FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_course_document_group (
  group_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  group_name VARCHAR(150) NOT NULL,
  group_description TEXT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (course_id),
  CONSTRAINT fk_course_document_group_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_course_document (
  document_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  group_id BIGINT UNSIGNED NULL,
  title VARCHAR(255) NULL,
  document JSON NOT NULL,
  document_type VARCHAR(100) NULL,
  file_name VARCHAR(255) NULL,
  INDEX (course_id),
  INDEX (group_id),
  CONSTRAINT fk_course_document_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_course_document_group FOREIGN KEY (group_id) REFERENCES ems_course_document_group(group_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_market_trend_document (
  document_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NULL,
  document JSON NOT NULL,
  document_type VARCHAR(100) NULL,
  INDEX (trend_id),
  CONSTRAINT fk_market_trend_document_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE IF NOT EXISTS ems_job_post_document (
  document_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NULL,
  document JSON NOT NULL,
  document_type VARCHAR(100) NULL,
  file_name VARCHAR(255) NULL,
  INDEX (job_post_id),
  CONSTRAINT fk_job_post_document_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- End of schema for ems_recruitment_portal

-- ============================================================================
-- EXTENDED SCHEMA: Child Tables and Additional Links
-- Added: 2026-02-20
-- Total New Tables: 45 (39 child tables + 6 cross-entity links)
-- ============================================================================

-- ============================================================================
-- USER CHILD TABLES (7 tables)
-- ============================================================================

-- User Education History
CREATE TABLE IF NOT EXISTS ems_user_education (
  education_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  institution_id BIGINT UNSIGNED NULL,
  degree_type VARCHAR(100) NOT NULL COMMENT 'Bachelor, Master, PhD, Diploma, Certificate',
  field_of_study VARCHAR(255) NOT NULL,
  specialization VARCHAR(255) NULL,
  start_date DATE NOT NULL,
  end_date DATE NULL COMMENT 'NULL for ongoing education',
  grade_gpa VARCHAR(50) NULL,
  is_verified TINYINT(1) DEFAULT 0,
  certificate_document_id BIGINT UNSIGNED NULL,
  INDEX (user_id),
  INDEX (institution_id),
  CONSTRAINT fk_user_education_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_education_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Work Experience
CREATE TABLE IF NOT EXISTS ems_user_work_experience (
  experience_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  institution_id BIGINT UNSIGNED NULL,
  job_title VARCHAR(255) NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  employment_type ENUM('Full-time','Part-time','Contract','Internship','Freelance') DEFAULT 'Full-time',
  location VARCHAR(255) NULL,
  start_date DATE NOT NULL,
  end_date DATE NULL COMMENT 'NULL for current position',
  is_current TINYINT(1) DEFAULT 0,
  responsibilities TEXT NULL,
  achievements TEXT NULL,
  skills_used JSON NULL COMMENT 'Array of skills used in this role',
  INDEX (user_id),
  INDEX (institution_id),
  CONSTRAINT fk_user_experience_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_experience_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Skills
CREATE TABLE IF NOT EXISTS ems_user_skill (
  skill_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  skill_name VARCHAR(255) NOT NULL,
  skill_category VARCHAR(100) NULL COMMENT 'Technical, Soft, Language, Tool',
  proficiency_level ENUM('Beginner','Intermediate','Advanced','Expert') DEFAULT 'Intermediate',
  years_of_experience INT NULL,
  is_verified TINYINT(1) DEFAULT 0,
  verified_by_institution_id BIGINT UNSIGNED NULL,
  endorsement_count INT DEFAULT 0,
  INDEX (user_id),
  INDEX (verified_by_institution_id),
  CONSTRAINT fk_user_skill_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_skill_institution FOREIGN KEY (verified_by_institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Certifications
CREATE TABLE IF NOT EXISTS ems_user_certification (
  certification_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  certification_name VARCHAR(255) NOT NULL,
  issuing_organization VARCHAR(255) NOT NULL,
  institution_id BIGINT UNSIGNED NULL,
  issue_date DATE NOT NULL,
  expiry_date DATE NULL,
  credential_id VARCHAR(255) NULL,
  credential_url VARCHAR(500) NULL,
  certificate_document_id BIGINT UNSIGNED NULL,
  is_verified TINYINT(1) DEFAULT 0,
  INDEX (user_id),
  INDEX (institution_id),
  CONSTRAINT fk_user_certification_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_user_certification_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Languages
CREATE TABLE IF NOT EXISTS ems_user_language (
  language_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  language_name VARCHAR(100) NOT NULL,
  proficiency_level ENUM('Basic','Conversational','Professional','Native') DEFAULT 'Conversational',
  can_read TINYINT(1) DEFAULT 1,
  can_write TINYINT(1) DEFAULT 1,
  can_speak TINYINT(1) DEFAULT 1,
  INDEX (user_id),
  CONSTRAINT fk_user_language_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Achievements
CREATE TABLE IF NOT EXISTS ems_user_achievement (
  achievement_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NULL,
  achievement_type VARCHAR(100) NULL COMMENT 'Award, Publication, Patent, Project, Competition',
  issuer VARCHAR(255) NULL,
  date_achieved DATE NULL,
  url VARCHAR(500) NULL,
  document_id BIGINT UNSIGNED NULL,
  INDEX (user_id),
  CONSTRAINT fk_user_achievement_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Social Links
CREATE TABLE IF NOT EXISTS ems_user_social_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  platform VARCHAR(100) NOT NULL COMMENT 'LinkedIn, GitHub, Portfolio, Twitter, etc.',
  profile_url VARCHAR(500) NOT NULL,
  is_verified TINYINT(1) DEFAULT 0,
  INDEX (user_id),
  CONSTRAINT fk_user_social_link_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- INSTITUTION CHILD TABLES (5 tables)
-- ============================================================================

-- Institution Departments
CREATE TABLE IF NOT EXISTS ems_institution_department (
  department_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  department_name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  head_of_department_user_id BIGINT UNSIGNED NULL,
  contact_email VARCHAR(255) NULL,
  contact_phone VARCHAR(30) NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (institution_id),
  INDEX (head_of_department_user_id),
  CONSTRAINT fk_department_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE,
  CONSTRAINT fk_department_head FOREIGN KEY (head_of_department_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Institution Locations
CREATE TABLE IF NOT EXISTS ems_institution_location (
  location_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  location_type ENUM('Main Campus','Branch','Office','Training Center') DEFAULT 'Branch',
  address_line1 VARCHAR(255) NOT NULL,
  address_line2 VARCHAR(255) NULL,
  city VARCHAR(100) NOT NULL,
  state_province VARCHAR(100) NULL,
  country VARCHAR(100) NOT NULL,
  postal_code VARCHAR(20) NULL,
  latitude DECIMAL(10,8) NULL,
  longitude DECIMAL(11,8) NULL,
  is_primary TINYINT(1) DEFAULT 0,
  INDEX (institution_id),
  CONSTRAINT fk_location_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Institution Accreditations
CREATE TABLE IF NOT EXISTS ems_institution_accreditation (
  accreditation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  accrediting_body VARCHAR(255) NOT NULL,
  accreditation_type VARCHAR(255) NULL,
  accreditation_level VARCHAR(100) NULL,
  issue_date DATE NOT NULL,
  expiry_date DATE NULL,
  certificate_document_id BIGINT UNSIGNED NULL,
  is_active TINYINT(1) DEFAULT 1,
  INDEX (institution_id),
  CONSTRAINT fk_accreditation_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Institution Rankings
CREATE TABLE IF NOT EXISTS ems_institution_ranking (
  ranking_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  ranking_organization VARCHAR(255) NOT NULL COMMENT 'QS, Times Higher Ed, etc.',
  ranking_year INT NOT NULL,
  overall_rank INT NULL,
  country_rank INT NULL,
  category VARCHAR(255) NULL,
  category_rank INT NULL,
  score DECIMAL(5,2) NULL,
  INDEX (institution_id),
  CONSTRAINT fk_ranking_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Institution Facilities
CREATE TABLE IF NOT EXISTS ems_institution_facility (
  facility_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  facility_name VARCHAR(255) NOT NULL,
  facility_type VARCHAR(100) NULL COMMENT 'Library, Lab, Sports, Hostel, Cafeteria, etc.',
  description TEXT NULL,
  capacity INT NULL,
  location_id BIGINT UNSIGNED NULL,
  is_available TINYINT(1) DEFAULT 1,
  INDEX (institution_id),
  INDEX (location_id),
  CONSTRAINT fk_facility_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE,
  CONSTRAINT fk_facility_location FOREIGN KEY (location_id) REFERENCES ems_institution_location(location_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- COURSE CHILD TABLES (8 tables)
-- ============================================================================

-- Course Modules
CREATE TABLE IF NOT EXISTS ems_course_module (
  module_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  module_name VARCHAR(255) NOT NULL,
  module_number INT NOT NULL,
  description TEXT NULL,
  duration_hours INT NULL,
  learning_objectives TEXT NULL,
  is_mandatory TINYINT(1) DEFAULT 1,
  order_sequence INT NOT NULL,
  INDEX (course_id),
  CONSTRAINT fk_module_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course Lessons
CREATE TABLE IF NOT EXISTS ems_course_lesson (
  lesson_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  module_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  lesson_title VARCHAR(255) NOT NULL,
  lesson_number INT NOT NULL,
  content_type ENUM('Video','Text','Quiz','Assignment','Live Session') DEFAULT 'Video',
  content_url VARCHAR(500) NULL,
  duration_minutes INT NULL,
  is_preview_available TINYINT(1) DEFAULT 0,
  order_sequence INT NOT NULL,
  INDEX (module_id),
  INDEX (course_id),
  CONSTRAINT fk_lesson_module FOREIGN KEY (module_id) REFERENCES ems_course_module(module_id) ON DELETE CASCADE,
  CONSTRAINT fk_lesson_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course Prerequisites
CREATE TABLE IF NOT EXISTS ems_course_prerequisite (
  prerequisite_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  prerequisite_course_id BIGINT UNSIGNED NULL,
  prerequisite_type ENUM('Course','Skill','Certification','Experience') DEFAULT 'Course',
  prerequisite_description TEXT NULL,
  is_mandatory TINYINT(1) DEFAULT 1,
  INDEX (course_id),
  INDEX (prerequisite_course_id),
  CONSTRAINT fk_prerequisite_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_prerequisite_prereq_course FOREIGN KEY (prerequisite_course_id) REFERENCES ems_course(course_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course Instructors
CREATE TABLE IF NOT EXISTS ems_course_instructor (
  instructor_link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  role ENUM('Lead Instructor','Co-Instructor','Teaching Assistant','Guest Lecturer') DEFAULT 'Lead Instructor',
  bio TEXT NULL,
  specialization VARCHAR(255) NULL,
  INDEX (course_id),
  INDEX (user_id),
  CONSTRAINT fk_instructor_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_instructor_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course Reviews
CREATE TABLE IF NOT EXISTS ems_course_review (
  review_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  rating DECIMAL(2,1) NOT NULL COMMENT '1.0 to 5.0',
  review_title VARCHAR(255) NULL,
  review_text TEXT NULL,
  helpful_count INT DEFAULT 0,
  is_verified_purchase TINYINT(1) DEFAULT 0,
  INDEX (course_id),
  INDEX (user_id),
  CONSTRAINT fk_review_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT chk_rating CHECK (rating >= 1.0 AND rating <= 5.0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course Assignments
CREATE TABLE IF NOT EXISTS ems_course_assignment (
  assignment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  module_id BIGINT UNSIGNED NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT NULL,
  assignment_type ENUM('Quiz','Project','Essay','Practical','Exam') DEFAULT 'Quiz',
  max_score INT NOT NULL DEFAULT 100,
  passing_score INT NOT NULL DEFAULT 60,
  due_date TIMESTAMP NULL,
  duration_minutes INT NULL,
  is_mandatory TINYINT(1) DEFAULT 1,
  INDEX (course_id),
  INDEX (module_id),
  CONSTRAINT fk_assignment_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_assignment_module FOREIGN KEY (module_id) REFERENCES ems_course_module(module_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Course Progress
CREATE TABLE IF NOT EXISTS ems_user_course_progress (
  progress_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  lesson_id BIGINT UNSIGNED NULL,
  completion_percentage DECIMAL(5,2) DEFAULT 0.00,
  last_accessed_at TIMESTAMP NULL,
  time_spent_minutes INT DEFAULT 0,
  status ENUM('Not Started','In Progress','Completed','Dropped') DEFAULT 'Not Started',
  INDEX (user_id),
  INDEX (course_id),
  INDEX (lesson_id),
  CONSTRAINT fk_progress_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_progress_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_progress_lesson FOREIGN KEY (lesson_id) REFERENCES ems_course_lesson(lesson_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Assignment Submissions
CREATE TABLE IF NOT EXISTS ems_user_assignment_submission (
  submission_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  assignment_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  submission_content TEXT NULL,
  submission_file_id BIGINT UNSIGNED NULL,
  submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  score INT NULL,
  feedback TEXT NULL,
  graded_by_user_id BIGINT UNSIGNED NULL,
  graded_at TIMESTAMP NULL,
  status ENUM('Submitted','Graded','Resubmit Required') DEFAULT 'Submitted',
  INDEX (assignment_id),
  INDEX (user_id),
  INDEX (graded_by_user_id),
  CONSTRAINT fk_submission_assignment FOREIGN KEY (assignment_id) REFERENCES ems_course_assignment(assignment_id) ON DELETE CASCADE,
  CONSTRAINT fk_submission_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_submission_grader FOREIGN KEY (graded_by_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- JOB POST CHILD TABLES (6 tables)
-- ============================================================================

-- Job Post Requirements
CREATE TABLE IF NOT EXISTS ems_job_post_requirement (
  requirement_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  requirement_type ENUM('Education','Experience','Skill','Certification','Language') NOT NULL,
  requirement_description TEXT NOT NULL,
  is_mandatory TINYINT(1) DEFAULT 1,
  minimum_years INT NULL COMMENT 'For experience requirements',
  proficiency_level VARCHAR(100) NULL,
  INDEX (job_post_id),
  CONSTRAINT fk_requirement_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Post Benefits
CREATE TABLE IF NOT EXISTS ems_job_post_benefit (
  benefit_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  benefit_type VARCHAR(100) NOT NULL COMMENT 'Health Insurance, Retirement, Vacation, Remote Work, etc.',
  benefit_description TEXT NULL,
  INDEX (job_post_id),
  CONSTRAINT fk_benefit_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Applications
CREATE TABLE IF NOT EXISTS ems_job_application (
  application_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  cover_letter TEXT NULL,
  resume_document_id BIGINT UNSIGNED NULL,
  application_status ENUM('Applied','Under Review','Shortlisted','Interview Scheduled','Rejected','Accepted','Withdrawn') DEFAULT 'Applied',
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  status_updated_at TIMESTAMP NULL,
  status_updated_by_user_id BIGINT UNSIGNED NULL,
  notes TEXT NULL,
  INDEX (job_post_id),
  INDEX (user_id),
  INDEX (status_updated_by_user_id),
  CONSTRAINT fk_application_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE,
  CONSTRAINT fk_application_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_application_status_updater FOREIGN KEY (status_updated_by_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Interviews
CREATE TABLE IF NOT EXISTS ems_job_interview (
  interview_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  application_id BIGINT UNSIGNED NOT NULL,
  interview_type ENUM('Phone Screen','Video','In-Person','Technical','HR','Final') DEFAULT 'Phone Screen',
  interview_round INT DEFAULT 1,
  scheduled_at TIMESTAMP NOT NULL,
  duration_minutes INT DEFAULT 60,
  location VARCHAR(255) NULL,
  meeting_link VARCHAR(500) NULL,
  interviewer_user_id BIGINT UNSIGNED NULL,
  status ENUM('Scheduled','Completed','Cancelled','Rescheduled') DEFAULT 'Scheduled',
  feedback TEXT NULL,
  rating DECIMAL(2,1) NULL COMMENT '1.0 to 5.0',
  INDEX (application_id),
  INDEX (interviewer_user_id),
  CONSTRAINT fk_interview_application FOREIGN KEY (application_id) REFERENCES ems_job_application(application_id) ON DELETE CASCADE,
  CONSTRAINT fk_interview_interviewer FOREIGN KEY (interviewer_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Post Questions
CREATE TABLE IF NOT EXISTS ems_job_post_question (
  question_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  question_text TEXT NOT NULL,
  question_type ENUM('Text','Multiple Choice','Yes/No','File Upload') DEFAULT 'Text',
  is_required TINYINT(1) DEFAULT 0,
  order_sequence INT NOT NULL,
  INDEX (job_post_id),
  CONSTRAINT fk_question_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Application Answers
CREATE TABLE IF NOT EXISTS ems_job_application_answer (
  answer_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  application_id BIGINT UNSIGNED NOT NULL,
  question_id BIGINT UNSIGNED NOT NULL,
  answer_text TEXT NULL,
  answer_file_id BIGINT UNSIGNED NULL,
  INDEX (application_id),
  INDEX (question_id),
  CONSTRAINT fk_answer_application FOREIGN KEY (application_id) REFERENCES ems_job_application(application_id) ON DELETE CASCADE,
  CONSTRAINT fk_answer_question FOREIGN KEY (question_id) REFERENCES ems_job_post_question(question_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- COMMUNITY CHILD TABLES (7 tables)
-- ============================================================================

-- Community Categories
CREATE TABLE IF NOT EXISTS ems_community_category (
  category_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  category_name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  icon VARCHAR(100) NULL,
  color VARCHAR(50) NULL,
  order_sequence INT NOT NULL,
  INDEX (community_id),
  CONSTRAINT fk_category_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Community Rules
CREATE TABLE IF NOT EXISTS ems_community_rule (
  rule_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  rule_title VARCHAR(255) NOT NULL,
  rule_description TEXT NOT NULL,
  order_sequence INT NOT NULL,
  INDEX (community_id),
  CONSTRAINT fk_rule_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Community Events
CREATE TABLE IF NOT EXISTS ems_community_event (
  event_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  event_title VARCHAR(255) NOT NULL,
  description TEXT NULL,
  event_type ENUM('Webinar','Workshop','Meetup','Conference','Social') DEFAULT 'Meetup',
  start_datetime TIMESTAMP NOT NULL,
  end_datetime TIMESTAMP NOT NULL,
  location VARCHAR(255) NULL,
  meeting_link VARCHAR(500) NULL,
  max_attendees INT NULL,
  organizer_user_id BIGINT UNSIGNED NOT NULL,
  INDEX (community_id),
  INDEX (organizer_user_id),
  CONSTRAINT fk_event_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE,
  CONSTRAINT fk_event_organizer FOREIGN KEY (organizer_user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Community Event Attendees
CREATE TABLE IF NOT EXISTS ems_community_event_attendee (
  attendee_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  event_id BIGINT UNSIGNED NOT NULL,
  user_id BIGINT UNSIGNED NOT NULL,
  rsvp_status ENUM('Going','Maybe','Not Going','Waitlist') DEFAULT 'Going',
  attended TINYINT(1) DEFAULT 0,
  INDEX (event_id),
  INDEX (user_id),
  CONSTRAINT fk_attendee_event FOREIGN KEY (event_id) REFERENCES ems_community_event(event_id) ON DELETE CASCADE,
  CONSTRAINT fk_attendee_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Post Attachments
CREATE TABLE IF NOT EXISTS ems_post_attachment (
  attachment_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  post_id BIGINT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  file_type VARCHAR(100) NULL COMMENT 'image, video, document, audio',
  file_url VARCHAR(500) NOT NULL,
  file_size_kb INT NULL,
  thumbnail_url VARCHAR(500) NULL,
  INDEX (post_id),
  CONSTRAINT fk_attachment_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Post Tags
CREATE TABLE IF NOT EXISTS ems_post_tag (
  tag_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  tag_name VARCHAR(100) NOT NULL UNIQUE,
  description TEXT NULL,
  usage_count INT DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Post Tag Links
CREATE TABLE IF NOT EXISTS ems_post_tag_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  post_id BIGINT UNSIGNED NOT NULL,
  tag_id BIGINT UNSIGNED NOT NULL,
  INDEX (post_id),
  INDEX (tag_id),
  CONSTRAINT fk_post_tag_link_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE,
  CONSTRAINT fk_post_tag_link_tag FOREIGN KEY (tag_id) REFERENCES ems_post_tag(tag_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- MARKET TREND CHILD TABLES (3 tables)
-- ============================================================================

-- Market Trend Skill Demand
CREATE TABLE IF NOT EXISTS ems_market_trend_skill_demand (
  demand_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  skill_name VARCHAR(255) NOT NULL,
  demand_level ENUM('Low','Medium','High','Very High') DEFAULT 'Medium',
  growth_rate DECIMAL(5,2) NULL COMMENT 'Percentage growth rate',
  average_salary_range VARCHAR(100) NULL,
  job_openings_count INT NULL,
  region VARCHAR(255) NULL,
  industry VARCHAR(255) NULL,
  INDEX (trend_id),
  CONSTRAINT fk_skill_demand_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend Industry
CREATE TABLE IF NOT EXISTS ems_market_trend_industry (
  industry_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  industry_name VARCHAR(255) NOT NULL,
  description TEXT NULL,
  growth_rate DECIMAL(5,2) NULL COMMENT 'Percentage growth rate',
  market_size VARCHAR(100) NULL,
  key_players TEXT NULL COMMENT 'Major companies in this industry',
  emerging_technologies TEXT NULL,
  INDEX (trend_id),
  CONSTRAINT fk_industry_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend Location
CREATE TABLE IF NOT EXISTS ems_market_trend_location (
  location_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  country VARCHAR(100) NOT NULL,
  region VARCHAR(255) NULL,
  city VARCHAR(100) NULL,
  job_market_health ENUM('Weak','Fair','Good','Excellent') DEFAULT 'Fair',
  unemployment_rate DECIMAL(5,2) NULL,
  average_salary VARCHAR(100) NULL,
  cost_of_living_index DECIMAL(5,2) NULL,
  top_industries TEXT NULL,
  INDEX (trend_id),
  CONSTRAINT fk_location_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- CROSS-ENTITY TABLES (3 tables)
-- ============================================================================

-- User Skill Endorsements
CREATE TABLE IF NOT EXISTS ems_user_skill_endorsement (
  endorsement_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  skill_id BIGINT UNSIGNED NOT NULL,
  endorsed_by_user_id BIGINT UNSIGNED NOT NULL,
  endorsement_comment TEXT NULL,
  relationship VARCHAR(100) NULL COMMENT 'Colleague, Manager, Client, etc.',
  INDEX (skill_id),
  INDEX (endorsed_by_user_id),
  CONSTRAINT fk_endorsement_skill FOREIGN KEY (skill_id) REFERENCES ems_user_skill(skill_id) ON DELETE CASCADE,
  CONSTRAINT fk_endorsement_endorser FOREIGN KEY (endorsed_by_user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- User Recommendations
CREATE TABLE IF NOT EXISTS ems_user_recommendation (
  recommendation_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL COMMENT 'User being recommended',
  recommended_by_user_id BIGINT UNSIGNED NOT NULL,
  recommendation_text TEXT NOT NULL,
  relationship VARCHAR(100) NULL COMMENT 'Colleague, Manager, Client, etc.',
  position_at_time VARCHAR(255) NULL,
  is_visible TINYINT(1) DEFAULT 1,
  INDEX (user_id),
  INDEX (recommended_by_user_id),
  CONSTRAINT fk_recommendation_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE,
  CONSTRAINT fk_recommendation_recommender FOREIGN KEY (recommended_by_user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Notifications
CREATE TABLE IF NOT EXISTS ems_notification (
  notification_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  notification_type VARCHAR(100) NOT NULL COMMENT 'Job Application, Course Update, Community Post, etc.',
  title VARCHAR(255) NOT NULL,
  message TEXT NOT NULL,
  related_entity_type VARCHAR(100) NULL COMMENT 'job_post, course, community, etc.',
  related_entity_id BIGINT UNSIGNED NULL,
  action_url VARCHAR(500) NULL,
  is_read TINYINT(1) DEFAULT 0,
  read_at TIMESTAMP NULL,
  priority ENUM('Low','Normal','High','Urgent') DEFAULT 'Normal',
  INDEX (user_id),
  INDEX (is_read),
  CONSTRAINT fk_notification_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- MISSING CROSS-ENTITY LINK TABLES (6 tables)
-- ============================================================================

-- Course-Job Post Link (Skills alignment)
CREATE TABLE IF NOT EXISTS ems_course_job_post_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  job_post_id BIGINT UNSIGNED NOT NULL,
  relevance_score DECIMAL(3,2) NULL COMMENT '0.00 to 1.00 - how relevant the course is to the job',
  matching_skills JSON NULL COMMENT 'Array of skills that match between course and job',
  ai_generated TINYINT(1) DEFAULT 0,
  INDEX (course_id),
  INDEX (job_post_id),
  CONSTRAINT fk_course_job_link_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_course_job_link_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course-Community Link (Discussion groups for courses)
CREATE TABLE IF NOT EXISTS ems_course_community_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  community_id BIGINT UNSIGNED NOT NULL,
  link_type ENUM('Official','Study Group','Alumni','Discussion') DEFAULT 'Discussion',
  is_active TINYINT(1) DEFAULT 1,
  INDEX (course_id),
  INDEX (community_id),
  CONSTRAINT fk_course_comm_link_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_course_comm_link_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Post-Community Link (Job postings in communities)
CREATE TABLE IF NOT EXISTS ems_job_post_community_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  community_id BIGINT UNSIGNED NOT NULL,
  is_featured TINYINT(1) DEFAULT 0,
  posted_by_user_id BIGINT UNSIGNED NULL,
  INDEX (job_post_id),
  INDEX (community_id),
  INDEX (posted_by_user_id),
  CONSTRAINT fk_job_comm_link_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE,
  CONSTRAINT fk_job_comm_link_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE,
  CONSTRAINT fk_job_comm_link_poster FOREIGN KEY (posted_by_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend-Course Link (Trending courses based on market demand)
CREATE TABLE IF NOT EXISTS ems_market_trend_course_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  course_id BIGINT UNSIGNED NOT NULL,
  relevance_score DECIMAL(3,2) NULL COMMENT '0.00 to 1.00 - how relevant the course is to the trend',
  demand_level ENUM('Low','Medium','High','Very High') DEFAULT 'Medium',
  recommendation_reason TEXT NULL,
  ai_generated TINYINT(1) DEFAULT 1,
  INDEX (trend_id),
  INDEX (course_id),
  CONSTRAINT fk_trend_course_link_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE,
  CONSTRAINT fk_trend_course_link_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend-Job Post Link (Trending jobs based on market analysis)
CREATE TABLE IF NOT EXISTS ems_market_trend_job_post_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  job_post_id BIGINT UNSIGNED NOT NULL,
  relevance_score DECIMAL(3,2) NULL COMMENT '0.00 to 1.00 - how relevant the job is to the trend',
  growth_potential ENUM('Low','Medium','High','Very High') DEFAULT 'Medium',
  salary_trend VARCHAR(100) NULL COMMENT 'Increasing, Stable, Decreasing',
  ai_generated TINYINT(1) DEFAULT 1,
  INDEX (trend_id),
  INDEX (job_post_id),
  CONSTRAINT fk_trend_job_link_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE,
  CONSTRAINT fk_trend_job_link_job FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend-Institution Link (Institutions aligned with market trends)
CREATE TABLE IF NOT EXISTS ems_market_trend_institution_link (
  link_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  institution_id BIGINT UNSIGNED NOT NULL,
  relevance_score DECIMAL(3,2) NULL COMMENT '0.00 to 1.00 - how aligned the institution is with the trend',
  specialization_areas TEXT NULL COMMENT 'Areas where institution excels in this trend',
  partnership_opportunities TEXT NULL,
  ai_generated TINYINT(1) DEFAULT 1,
  INDEX (trend_id),
  INDEX (institution_id),
  CONSTRAINT fk_trend_inst_link_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE,
  CONSTRAINT fk_trend_inst_link_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- End of Extended Schema
-- Total Tables Added: 45
--   - User child tables: 7
--   - Institution child tables: 5
--   - Course child tables: 8
--   - Job Post child tables: 6
--   - Community child tables: 7
--   - Market Trend child tables: 3
--   - Cross-entity tables: 3
--   - Missing link tables: 6
-- ============================================================================

-- ============================================================================
-- FILE UPLOAD TABLES FOR TOP-LEVEL ENTITIES
-- Added: 2026-02-20
-- Purpose: Handle file uploads including rich text and code editor content
-- ============================================================================

-- User File Uploads
CREATE TABLE IF NOT EXISTS ems_user_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id BIGINT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Resume, Certificate, Portfolio, Bio, Code Sample, etc.',
  is_verified TINYINT(1) DEFAULT 0,
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  INDEX (user_id),
  INDEX (file_type),
  INDEX (category),
  CONSTRAINT fk_user_file_user FOREIGN KEY (user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Institution File Uploads
CREATE TABLE IF NOT EXISTS ems_institution_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  institution_id BIGINT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Brochure, Accreditation, Logo, Campus Photos, Description, etc.',
  is_verified TINYINT(1) DEFAULT 0,
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  INDEX (institution_id),
  INDEX (file_type),
  INDEX (category),
  CONSTRAINT fk_institution_file_institution FOREIGN KEY (institution_id) REFERENCES ems_institution(institution_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Course File Uploads
CREATE TABLE IF NOT EXISTS ems_course_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  course_id BIGINT UNSIGNED NOT NULL,
  module_id BIGINT UNSIGNED NULL COMMENT 'Optional: link to specific module',
  lesson_id BIGINT UNSIGNED NULL COMMENT 'Optional: link to specific lesson',
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Lecture Notes, Assignment, Reading Material, Video Lecture, Lesson Content, Code Example, etc.',
  is_downloadable TINYINT(1) DEFAULT 1,
  requires_enrollment TINYINT(1) DEFAULT 1,
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  duration_seconds INT NULL COMMENT 'For video/audio files',
  INDEX (course_id),
  INDEX (module_id),
  INDEX (lesson_id),
  INDEX (file_type),
  INDEX (category),
  CONSTRAINT fk_course_file_course FOREIGN KEY (course_id) REFERENCES ems_course(course_id) ON DELETE CASCADE,
  CONSTRAINT fk_course_file_module FOREIGN KEY (module_id) REFERENCES ems_course_module(module_id) ON DELETE SET NULL,
  CONSTRAINT fk_course_file_lesson FOREIGN KEY (lesson_id) REFERENCES ems_course_lesson(lesson_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Job Post File Uploads
CREATE TABLE IF NOT EXISTS ems_job_post_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  job_post_id BIGINT UNSIGNED NOT NULL,
  application_id BIGINT UNSIGNED NULL COMMENT 'Optional: link to specific application',
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Job Description, Company Brochure, Resume, Cover Letter, Portfolio, Requirements, etc.',
  uploaded_by_user_id BIGINT UNSIGNED NULL COMMENT 'User who uploaded (applicant or recruiter)',
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  INDEX (job_post_id),
  INDEX (application_id),
  INDEX (file_type),
  INDEX (category),
  INDEX (uploaded_by_user_id),
  CONSTRAINT fk_job_post_file_job_post FOREIGN KEY (job_post_id) REFERENCES ems_job_post(job_post_id) ON DELETE CASCADE,
  CONSTRAINT fk_job_post_file_application FOREIGN KEY (application_id) REFERENCES ems_job_application(application_id) ON DELETE CASCADE,
  CONSTRAINT fk_job_post_file_uploader FOREIGN KEY (uploaded_by_user_id) REFERENCES ems_user(user_id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Community File Uploads
CREATE TABLE IF NOT EXISTS ems_community_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  community_id BIGINT UNSIGNED NOT NULL,
  post_id BIGINT UNSIGNED NULL COMMENT 'Optional: link to specific post',
  event_id BIGINT UNSIGNED NULL COMMENT 'Optional: link to specific event',
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Community Banner, Event Photo, Shared Document, Post Content, Code Snippet, etc.',
  uploaded_by_user_id BIGINT UNSIGNED NOT NULL,
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  INDEX (community_id),
  INDEX (post_id),
  INDEX (event_id),
  INDEX (file_type),
  INDEX (category),
  INDEX (uploaded_by_user_id),
  CONSTRAINT fk_community_file_community FOREIGN KEY (community_id) REFERENCES ems_community(community_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_file_post FOREIGN KEY (post_id) REFERENCES ems_community_user_post(post_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_file_event FOREIGN KEY (event_id) REFERENCES ems_community_event(event_id) ON DELETE CASCADE,
  CONSTRAINT fk_community_file_uploader FOREIGN KEY (uploaded_by_user_id) REFERENCES ems_user(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Market Trend File Uploads
CREATE TABLE IF NOT EXISTS ems_market_trend_file (
  file_id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  trend_id BIGINT UNSIGNED NOT NULL,
  file_name VARCHAR(255) NOT NULL,
  original_file_name VARCHAR(255) NOT NULL,
  file_type ENUM('pdf','image','video','audio','document','spreadsheet','presentation','archive','code','html','markdown','other') NOT NULL,
  file_extension VARCHAR(20) NULL,
  file_location VARCHAR(500) NOT NULL COMMENT 'Path or URL to the file',
  file_size_bytes BIGINT NULL,
  mime_type VARCHAR(100) NULL,
  description TEXT NULL,
  comment TEXT NULL,
  category VARCHAR(100) NULL COMMENT 'Report, Analysis, Chart, Infographic, Summary, etc.',
  source VARCHAR(255) NULL COMMENT 'Source of the data/report',
  report_date DATE NULL COMMENT 'Date of the report/analysis',
  download_count INT DEFAULT 0,
  thumbnail_location VARCHAR(500) NULL COMMENT 'For images and videos',
  INDEX (trend_id),
  INDEX (file_type),
  INDEX (category),
  CONSTRAINT fk_market_trend_file_trend FOREIGN KEY (trend_id) REFERENCES ems_ai_market_trend_property(trend_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================================
-- End of File Upload Tables
-- Total Tables Added: 6
--   - ems_user_file
--   - ems_institution_file
--   - ems_course_file
--   - ems_job_post_file
--   - ems_community_file
--   - ems_market_trend_file
-- ============================================================================

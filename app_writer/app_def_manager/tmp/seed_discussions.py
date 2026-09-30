"""Seed the discussion tracker with key items from this session."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from discussion_tracker.tracker import log_discussion, log_task, log_decision

# Decisions
log_decision("App architecture: job portal", "Build a job portal with students, employers, trainers interacting", "Three user types, subscription-based access via authorization groups", tags=["architecture"], app="job_portal")
log_decision("User roles via authorization groups", "No role fields on UserProfile — access controlled entirely through authorization groups (table/query access)", "Users get default USER role, subscription determines table access", tags=["auth", "architecture"], app="job_portal")
log_decision("Single record per user", "Profile entities (UserProfile, StudentProfile, EmployerProfile, TrainerProfile) allow only one record per user", "Implemented singleRecordPerUser flag across swfaw/reaw/app_def_manager", tags=["feature", "singleRecordPerUser"], app="job_portal")
log_decision("Common profile fields", "Extracted common fields (firstName, lastName, email, phone, bio) into UserProfile", "Role-specific profiles keep only their unique fields", tags=["refactoring"], app="job_portal")

# Discussions
log_discussion("Entity design", "Designed 33 entities across profiles, user data, jobs, training, course content, Q&A, and masters", "Entities organized into categories: Profile(4), User Data(3), Jobs(2), Training(7), Course Content(4), Q&A(4), Master(9)", tags=["entities"], app="job_portal")
log_discussion("React UI structure", "Defined navigation with 7 groups: Dashboard, My Profile, My Resume, Jobs, Training, My Learning, Masters", "Tabbed forms for Profile, Resume, Training Program, Exams, Q&A groups", tags=["react", "ui"], app="job_portal")
log_discussion("Theme selection", "Scraped Sakai PrimeReact theme for the job portal", "Indigo accent (#6366F1), Inter font, clean light background", tags=["theme", "react"], app="job_portal")

# Tasks
log_task("Add entity relationships", "Define FK relationships between all 33 entities (e.g., JobApplication→StudentProfile+JobPosting)", "Relationships not yet added to webflux_relationships.json", priority="high", tags=["relationships"], app="job_portal")
log_task("Fix React register page", "Register page shows warning: missing input field", "Frontend validator flagged /register as warning", priority="normal", tags=["react", "bug"], app="job_portal")
log_task("Enable CORS for production", "Configure proper CORS origins for production deployment", "Currently allows localhost origins + null", priority="normal", tags=["security", "deployment"], app="job_portal")
log_task("Generate dummy data", "Generate seed data for all 33 entities using Dummy Data Generator", "Database has schema but no test data", priority="normal", tags=["data"], app="job_portal")
log_task("Build workspace web app", "Browser-based UI for all workspace tools", "Spec at .kiro/specs/workspace-web-app/. FastAPI + Kafka + React", priority="low", tags=["tooling"], app="workspace")

print("Done seeding discussions!")

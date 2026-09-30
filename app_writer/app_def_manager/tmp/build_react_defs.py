"""Build React definition files for job_portal."""
import json
from pathlib import Path

app_dir = Path("application_definitions/job_portal")

# ── Routes ──────────────────────────────────────────────────────────────────
routes = [
    {"path": "/", "pageComponent": "DashboardPage", "pageType": "entity", "pageFolder": "dashboard", "entityName": "Dashboard", "navLabel": "Dashboard", "navGroup": "Dashboard", "requiresAuth": True},
    # My Profile
    {"path": "/my-profile", "pageComponent": "UserProfilePage", "pageType": "entity", "pageFolder": "profiles", "entityName": "UserProfile", "navLabel": "My Profile", "navGroup": "My Profile", "requiresAuth": True},
    # My Resume
    {"path": "/my-resume", "pageComponent": "UserEducationPage", "pageType": "entity", "pageFolder": "resume", "entityName": "UserEducation", "navLabel": "My Resume", "navGroup": "My Resume", "requiresAuth": True},
    # Jobs
    {"path": "/jobs", "pageComponent": "JobPostingPage", "pageType": "entity", "pageFolder": "jobs", "entityName": "JobPosting", "navLabel": "Browse Jobs", "navGroup": "Jobs", "requiresAuth": True},
    {"path": "/my-applications", "pageComponent": "JobApplicationPage", "pageType": "entity", "pageFolder": "jobs", "entityName": "JobApplication", "navLabel": "My Applications", "navGroup": "Jobs", "requiresAuth": True},
    # Training
    {"path": "/training-programs", "pageComponent": "TrainingProgramPage", "pageType": "entity", "pageFolder": "training", "entityName": "TrainingProgram", "navLabel": "Programs", "navGroup": "Training", "requiresAuth": True},
    {"path": "/exams", "pageComponent": "TrainingExamPage", "pageType": "entity", "pageFolder": "training", "entityName": "TrainingExam", "navLabel": "Exams", "navGroup": "Training", "requiresAuth": True},
    {"path": "/qa", "pageComponent": "CourseQuestionPage", "pageType": "entity", "pageFolder": "training", "entityName": "CourseQuestion", "navLabel": "Q&A", "navGroup": "Training", "requiresAuth": True},
    # My Learning
    {"path": "/my-enrollments", "pageComponent": "TrainingEnrollmentPage", "pageType": "entity", "pageFolder": "learning", "entityName": "TrainingEnrollment", "navLabel": "Enrollments", "navGroup": "My Learning", "requiresAuth": True},
    {"path": "/my-certifications", "pageComponent": "TrainingCertificationPage", "pageType": "entity", "pageFolder": "learning", "entityName": "TrainingCertification", "navLabel": "Certifications", "navGroup": "My Learning", "requiresAuth": True},
    # Masters
    {"path": "/masters/education-levels", "pageComponent": "EducationLevelPage", "pageType": "entity", "pageFolder": "masters", "entityName": "EducationLevel", "navLabel": "Education Levels", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/fields-of-study", "pageComponent": "FieldOfStudyPage", "pageType": "entity", "pageFolder": "masters", "entityName": "FieldOfStudy", "navLabel": "Fields of Study", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/institutions", "pageComponent": "InstitutionPage", "pageType": "entity", "pageFolder": "masters", "entityName": "Institution", "navLabel": "Institutions", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/industries", "pageComponent": "IndustryPage", "pageType": "entity", "pageFolder": "masters", "entityName": "Industry", "navLabel": "Industries", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/job-titles", "pageComponent": "JobTitlePage", "pageType": "entity", "pageFolder": "masters", "entityName": "JobTitle", "navLabel": "Job Titles", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/skill-categories", "pageComponent": "SkillCategoryPage", "pageType": "entity", "pageFolder": "masters", "entityName": "SkillCategory", "navLabel": "Skill Categories", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/skills", "pageComponent": "SkillPage", "pageType": "entity", "pageFolder": "masters", "entityName": "Skill", "navLabel": "Skills", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/companies", "pageComponent": "CompanyPage", "pageType": "entity", "pageFolder": "masters", "entityName": "Company", "navLabel": "Companies", "navGroup": "Masters", "requiresAuth": True},
    {"path": "/masters/locations", "pageComponent": "LocationPage", "pageType": "entity", "pageFolder": "masters", "entityName": "Location", "navLabel": "Locations", "navGroup": "Masters", "requiresAuth": True},
]

# ── Form Groupings (tabbed forms) ──────────────────────────────────────────
form_groupings = [
    {
        "groupName": "UserProfileGroup",
        "parentEntity": "UserProfile",
        "tabs": [
            {"entityName": "UserProfile", "tabLabel": "Basic Info", "tabOrder": 1},
            {"entityName": "StudentProfile", "tabLabel": "Student", "tabOrder": 2},
            {"entityName": "EmployerProfile", "tabLabel": "Employer", "tabOrder": 3},
            {"entityName": "TrainerProfile", "tabLabel": "Trainer", "tabOrder": 4},
        ]
    },
    {
        "groupName": "ResumeGroup",
        "parentEntity": "UserEducation",
        "tabs": [
            {"entityName": "UserEducation", "tabLabel": "Education", "tabOrder": 1},
            {"entityName": "UserWorkExperience", "tabLabel": "Work Experience", "tabOrder": 2},
            {"entityName": "UserSkill", "tabLabel": "Skills", "tabOrder": 3},
        ]
    },
    {
        "groupName": "TrainingProgramGroup",
        "parentEntity": "TrainingProgram",
        "tabs": [
            {"entityName": "TrainingProgram", "tabLabel": "Overview", "tabOrder": 1},
            {"entityName": "TrainingModule", "tabLabel": "Modules", "tabOrder": 2},
            {"entityName": "CourseDocument", "tabLabel": "Documents", "tabOrder": 3},
            {"entityName": "CourseVideo", "tabLabel": "Videos", "tabOrder": 4},
            {"entityName": "CourseAudio", "tabLabel": "Audio", "tabOrder": 5},
            {"entityName": "CourseCodeLab", "tabLabel": "Code Labs", "tabOrder": 6},
        ]
    },
    {
        "groupName": "ExamGroup",
        "parentEntity": "TrainingExam",
        "tabs": [
            {"entityName": "TrainingExam", "tabLabel": "Exam Details", "tabOrder": 1},
            {"entityName": "ExamQuestion", "tabLabel": "Questions", "tabOrder": 2},
            {"entityName": "ExamAnswer", "tabLabel": "Answers", "tabOrder": 3},
        ]
    },
    {
        "groupName": "QAGroup",
        "parentEntity": "CourseQuestion",
        "tabs": [
            {"entityName": "CourseQuestion", "tabLabel": "Questions", "tabOrder": 1},
            {"entityName": "CourseAnswer", "tabLabel": "Answers", "tabOrder": 2},
        ]
    },
]

# ── Write files ─────────────────────────────────────────────────────────────
(app_dir / "react_routes.json").write_text(json.dumps(routes, indent=2), encoding="utf-8")
print("  ✅ react_routes.json")

(app_dir / "react_form_groupings.json").write_text(json.dumps(form_groupings, indent=2), encoding="utf-8")
print("  ✅ react_form_groupings.json")

# Layout
layout = {
    "applicationName": "Job Portal",
    "apiPort": 8081,
    "header": {"visible": True, "collapsible": False, "defaultCollapsed": False},
    "footer": {"visible": True, "collapsible": False, "defaultCollapsed": False},
    "leftNav": {"visible": True, "collapsible": True, "defaultCollapsed": False},
    "content": {"visible": True, "collapsible": False, "defaultCollapsed": False},
    "navGroups": [
        {"groupName": "Dashboard", "entities": [{"label": "Dashboard", "path": "/"}]},
        {"groupName": "My Profile", "entities": [{"label": "My Profile", "path": "/my-profile"}]},
        {"groupName": "My Resume", "entities": [{"label": "My Resume", "path": "/my-resume"}]},
        {"groupName": "Jobs", "entities": [
            {"label": "Browse Jobs", "path": "/jobs"},
            {"label": "My Applications", "path": "/my-applications"},
        ]},
        {"groupName": "Training", "entities": [
            {"label": "Programs", "path": "/training-programs"},
            {"label": "Exams", "path": "/exams"},
            {"label": "Q&A", "path": "/qa"},
        ]},
        {"groupName": "My Learning", "entities": [
            {"label": "Enrollments", "path": "/my-enrollments"},
            {"label": "Certifications", "path": "/my-certifications"},
        ]},
        {"groupName": "Masters", "entities": [
            {"label": "Education Levels", "path": "/masters/education-levels"},
            {"label": "Fields of Study", "path": "/masters/fields-of-study"},
            {"label": "Institutions", "path": "/masters/institutions"},
            {"label": "Industries", "path": "/masters/industries"},
            {"label": "Job Titles", "path": "/masters/job-titles"},
            {"label": "Skill Categories", "path": "/masters/skill-categories"},
            {"label": "Skills", "path": "/masters/skills"},
            {"label": "Companies", "path": "/masters/companies"},
            {"label": "Locations", "path": "/masters/locations"},
        ]},
    ]
}
(app_dir / "react_layout.json").write_text(json.dumps(layout, indent=2), encoding="utf-8")
print("  ✅ react_layout.json")

# Auth config
auth_config = {
    "jwtEnabled": True,
    "oauth2Enabled": False,
    "oauth2Providers": [],
    "refreshTokenEnabled": True,
    "protectedRoutes": ["/my-profile", "/my-resume", "/jobs", "/my-applications",
                        "/training-programs", "/exams", "/qa", "/my-enrollments",
                        "/my-certifications", "/masters"],
    "permissionsEndpoint": "/api/auth/permissions",
    "loginEndpoint": "/api/auth/login",
    "registerEndpoint": "/api/auth/register",
    "registerEnabled": True
}
(app_dir / "react_auth_config.json").write_text(json.dumps(auth_config, indent=2), encoding="utf-8")
print("  ✅ react_auth_config.json")

print("\n✅ React definition files created!")

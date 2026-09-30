package com.jobportal.service;

import org.springframework.stereotype.Component;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Registry mapping database table names to their REST API base paths.
 * Auto-generated from controller layer definitions.
 */
@Component
public class EntityApiRegistry {

    private static final Map<String, String> TABLE_TO_PATH;

    static {
        Map<String, String> map = new LinkedHashMap<>();

        map.put("student_profile", "/api/student_profiles");

        map.put("employer_profile", "/api/employer_profiles");

        map.put("trainer_profile", "/api/trainer_profiles");

        map.put("job_posting", "/api/job_postings");

        map.put("training_program", "/api/training_programs");

        map.put("job_application", "/api/job_applications");

        map.put("training_enrollment", "/api/training_enrollments");

        map.put("user_profile", "/api/user_profiles");

        map.put("education_level", "/api/education_levels");

        map.put("field_of_study", "/api/field_of_studys");

        map.put("institution", "/api/institutions");

        map.put("user_education", "/api/user_educations");

        map.put("industry", "/api/industrys");

        map.put("job_title", "/api/job_titles");

        map.put("user_work_experience", "/api/user_work_experiences");

        map.put("skill_category", "/api/skill_categorys");

        map.put("skill", "/api/skills");

        map.put("user_skill", "/api/user_skills");

        map.put("training_module", "/api/training_modules");

        map.put("module_progress", "/api/module_progresss");

        map.put("training_exam", "/api/training_exams");

        map.put("exam_attempt", "/api/exam_attempts");

        map.put("training_certification", "/api/training_certifications");

        map.put("course_document", "/api/course_documents");

        map.put("course_video", "/api/course_videos");

        map.put("course_audio", "/api/course_audios");

        map.put("course_code_lab", "/api/course_code_labs");

        map.put("exam_question", "/api/exam_questions");

        map.put("exam_answer", "/api/exam_answers");

        map.put("course_question", "/api/course_questions");

        map.put("course_answer", "/api/course_answers");

        map.put("company", "/api/companys");

        map.put("location", "/api/locations");

        TABLE_TO_PATH = Collections.unmodifiableMap(map);
    }

    /**
     * Get the API base path for a table name.
     * @return base path or null if table has no API
     */
    public String getBasePath(String tableName) {
        return TABLE_TO_PATH.get(tableName);
    }

    /**
     * Get all table-to-path mappings.
     */
    public Map<String, String> getAllMappings() {
        return TABLE_TO_PATH;
    }
}
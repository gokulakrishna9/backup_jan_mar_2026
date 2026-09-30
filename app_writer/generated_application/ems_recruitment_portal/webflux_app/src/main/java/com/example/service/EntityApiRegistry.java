package com.example.service;

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

        map.put("ems_user", "/api/users");

        map.put("ems_user_property_group", "/api/userpropertygroups");

        map.put("ems_user_property", "/api/userpropertys");

        map.put("ems_institution", "/api/institutions");

        map.put("ems_institution_property_group", "/api/institutionpropertygroups");

        map.put("ems_institution_property", "/api/institutionpropertys");

        map.put("ems_candidate_institute_link", "/api/candidateinstitutelinks");

        map.put("ems_user_institute_property_link", "/api/userinstitutepropertylinks");

        map.put("ems_course", "/api/courses");

        map.put("ems_course_property_group", "/api/coursepropertygroups");

        map.put("ems_course_property", "/api/coursepropertys");

        map.put("ems_user_course_link", "/api/usercourselinks");

        map.put("ems_user_course_wishlist", "/api/usercoursewishlists");

        map.put("ems_user_course_purchase", "/api/usercoursepurchases");

        map.put("ems_job_post", "/api/jobposts");

        map.put("ems_job_post_property_group", "/api/jobpostpropertygroups");

        map.put("ems_job_post_property", "/api/jobpostpropertys");

        map.put("ems_user_job_post_bookmark", "/api/userjobpostbookmarks");

        map.put("ems_job_post_user_bookmark", "/api/jobpostuserbookmarks");

        map.put("ems_subscription_payment_history", "/api/subscriptionpaymenthistorys");

        map.put("ems_community", "/api/communitys");

        map.put("ems_community_property_group", "/api/communitypropertygroups");

        map.put("ems_community_property", "/api/communitypropertys");

        map.put("ems_community_user_link", "/api/communityuserlinks");

        map.put("ems_community_property_user_link", "/api/communitypropertyuserlinks");

        map.put("ems_community_user_post", "/api/communityuserposts");

        map.put("ems_community_post_link", "/api/communitypostlinks");

        map.put("ems_post_emogi", "/api/postemogis");

        map.put("ems_emogi_post_user_link", "/api/emogipostuserlinks");

        map.put("ems_post_flag", "/api/postflags");

        map.put("ems_post_comment", "/api/postcomments");

        map.put("ems_post_comment_emogi_link", "/api/postcommentemogilinks");

        map.put("ems_ai_user_profile_evaluation_parameter_group", "/api/aiuserprofileevaluationparametergroups");

        map.put("ems_ai_user_profile_evaluation_parameter", "/api/aiuserprofileevaluationparameters");

        map.put("ems_ai_user_profile_evaluation", "/api/aiuserprofileevaluations");

        map.put("ems_ai_evaluation_parameter_group", "/api/aievaluationparametergroups");

        map.put("ems_ai_evaluation_parameter", "/api/aievaluationparameters");

        map.put("ems_ai_institution_profile_evaluation", "/api/aiinstitutionprofileevaluations");

        map.put("ems_ai_job_recommendation", "/api/aijobrecommendations");

        map.put("ems_ai_community_post_evaluation", "/api/aicommunitypostevaluations");

        map.put("ems_ai_market_trend_parameter_group", "/api/aimarkettrendparametergroups");

        map.put("ems_ai_market_trend_parameter", "/api/aimarkettrendparameters");

        map.put("ems_ai_market_trend_property", "/api/aimarkettrendpropertys");

        map.put("ems_user_profile_document", "/api/userprofiledocuments");

        map.put("ems_institution_profile_document", "/api/institutionprofiledocuments");

        map.put("ems_course_document_group", "/api/coursedocumentgroups");

        map.put("ems_course_document", "/api/coursedocuments");

        map.put("ems_market_trend_document", "/api/markettrenddocuments");

        map.put("ems_job_post_document", "/api/jobpostdocuments");

        map.put("ems_user_education", "/api/usereducations");

        map.put("ems_user_work_experience", "/api/userworkexperiences");

        map.put("ems_user_skill", "/api/userskills");

        map.put("ems_user_certification", "/api/usercertifications");

        map.put("ems_user_language", "/api/userlanguages");

        map.put("ems_user_achievement", "/api/userachievements");

        map.put("ems_user_social_link", "/api/usersociallinks");

        map.put("ems_institution_department", "/api/institutiondepartments");

        map.put("ems_institution_location", "/api/institutionlocations");

        map.put("ems_institution_accreditation", "/api/institutionaccreditations");

        map.put("ems_institution_ranking", "/api/institutionrankings");

        map.put("ems_institution_facility", "/api/institutionfacilitys");

        map.put("ems_course_module", "/api/coursemodules");

        map.put("ems_course_lesson", "/api/courselessons");

        map.put("ems_course_prerequisite", "/api/courseprerequisites");

        map.put("ems_course_instructor", "/api/courseinstructors");

        map.put("ems_course_review", "/api/coursereviews");

        map.put("ems_course_assignment", "/api/courseassignments");

        map.put("ems_user_course_progress", "/api/usercourseprogresss");

        map.put("ems_user_assignment_submission", "/api/userassignmentsubmissions");

        map.put("ems_job_post_requirement", "/api/jobpostrequirements");

        map.put("ems_job_post_benefit", "/api/jobpostbenefits");

        map.put("ems_job_application", "/api/jobapplications");

        map.put("ems_job_interview", "/api/jobinterviews");

        map.put("ems_job_post_question", "/api/jobpostquestions");

        map.put("ems_job_application_answer", "/api/jobapplicationanswers");

        map.put("ems_community_category", "/api/communitycategorys");

        map.put("ems_community_rule", "/api/communityrules");

        map.put("ems_community_event", "/api/communityevents");

        map.put("ems_community_event_attendee", "/api/communityeventattendees");

        map.put("ems_post_attachment", "/api/postattachments");

        map.put("ems_post_tag", "/api/posttags");

        map.put("ems_post_tag_link", "/api/posttaglinks");

        map.put("ems_market_trend_skill_demand", "/api/markettrendskilldemands");

        map.put("ems_market_trend_industry", "/api/markettrendindustrys");

        map.put("ems_market_trend_location", "/api/markettrendlocations");

        map.put("ems_user_skill_endorsement", "/api/userskillendorsements");

        map.put("ems_user_recommendation", "/api/userrecommendations");

        map.put("ems_notification", "/api/notifications");

        map.put("ems_course_job_post_link", "/api/coursejobpostlinks");

        map.put("ems_course_community_link", "/api/coursecommunitylinks");

        map.put("ems_job_post_community_link", "/api/jobpostcommunitylinks");

        map.put("ems_market_trend_course_link", "/api/markettrendcourselinks");

        map.put("ems_market_trend_job_post_link", "/api/markettrendjobpostlinks");

        map.put("ems_market_trend_institution_link", "/api/markettrendinstitutionlinks");

        map.put("ems_user_file", "/api/userfiles");

        map.put("ems_institution_file", "/api/institutionfiles");

        map.put("ems_course_file", "/api/coursefiles");

        map.put("ems_job_post_file", "/api/jobpostfiles");

        map.put("ems_community_file", "/api/communityfiles");

        map.put("ems_market_trend_file", "/api/markettrendfiles");

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
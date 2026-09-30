import { configureStore } from '@reduxjs/toolkit';
import userReducer from './slices/userSlice';
import userPropertyGroupReducer from './slices/userPropertyGroupSlice';
import userPropertyReducer from './slices/userPropertySlice';
import institutionReducer from './slices/institutionSlice';
import institutionPropertyGroupReducer from './slices/institutionPropertyGroupSlice';
import institutionPropertyReducer from './slices/institutionPropertySlice';
import candidateInstituteLinkReducer from './slices/candidateInstituteLinkSlice';
import userInstitutePropertyLinkReducer from './slices/userInstitutePropertyLinkSlice';
import courseReducer from './slices/courseSlice';
import coursePropertyGroupReducer from './slices/coursePropertyGroupSlice';
import coursePropertyReducer from './slices/coursePropertySlice';
import userCourseLinkReducer from './slices/userCourseLinkSlice';
import userCourseWishlistReducer from './slices/userCourseWishlistSlice';
import userCoursePurchaseReducer from './slices/userCoursePurchaseSlice';
import jobPostReducer from './slices/jobPostSlice';
import jobPostPropertyGroupReducer from './slices/jobPostPropertyGroupSlice';
import jobPostPropertyReducer from './slices/jobPostPropertySlice';
import userJobPostBookmarkReducer from './slices/userJobPostBookmarkSlice';
import jobPostUserBookmarkReducer from './slices/jobPostUserBookmarkSlice';
import subscriptionPaymentHistoryReducer from './slices/subscriptionPaymentHistorySlice';
import communityReducer from './slices/communitySlice';
import communityPropertyGroupReducer from './slices/communityPropertyGroupSlice';
import communityPropertyReducer from './slices/communityPropertySlice';
import communityUserLinkReducer from './slices/communityUserLinkSlice';
import communityPropertyUserLinkReducer from './slices/communityPropertyUserLinkSlice';
import communityUserPostReducer from './slices/communityUserPostSlice';
import communityPostLinkReducer from './slices/communityPostLinkSlice';
import postEmogiReducer from './slices/postEmogiSlice';
import emogiPostUserLinkReducer from './slices/emogiPostUserLinkSlice';
import postFlagReducer from './slices/postFlagSlice';
import postCommentReducer from './slices/postCommentSlice';
import postCommentEmogiLinkReducer from './slices/postCommentEmogiLinkSlice';
import aiUserProfileEvaluationParameterGroupReducer from './slices/aiUserProfileEvaluationParameterGroupSlice';
import aiUserProfileEvaluationParameterReducer from './slices/aiUserProfileEvaluationParameterSlice';
import aiUserProfileEvaluationReducer from './slices/aiUserProfileEvaluationSlice';
import aiEvaluationParameterGroupReducer from './slices/aiEvaluationParameterGroupSlice';
import aiEvaluationParameterReducer from './slices/aiEvaluationParameterSlice';
import aiInstitutionProfileEvaluationReducer from './slices/aiInstitutionProfileEvaluationSlice';
import aiJobRecommendationReducer from './slices/aiJobRecommendationSlice';
import aiCommunityPostEvaluationReducer from './slices/aiCommunityPostEvaluationSlice';
import aiMarketTrendParameterGroupReducer from './slices/aiMarketTrendParameterGroupSlice';
import aiMarketTrendParameterReducer from './slices/aiMarketTrendParameterSlice';
import aiMarketTrendPropertyReducer from './slices/aiMarketTrendPropertySlice';
import userProfileDocumentReducer from './slices/userProfileDocumentSlice';
import institutionProfileDocumentReducer from './slices/institutionProfileDocumentSlice';
import courseDocumentGroupReducer from './slices/courseDocumentGroupSlice';
import courseDocumentReducer from './slices/courseDocumentSlice';
import marketTrendDocumentReducer from './slices/marketTrendDocumentSlice';
import jobPostDocumentReducer from './slices/jobPostDocumentSlice';
import userEducationReducer from './slices/userEducationSlice';
import userWorkExperienceReducer from './slices/userWorkExperienceSlice';
import userSkillReducer from './slices/userSkillSlice';
import userCertificationReducer from './slices/userCertificationSlice';
import userLanguageReducer from './slices/userLanguageSlice';
import userAchievementReducer from './slices/userAchievementSlice';
import userSocialLinkReducer from './slices/userSocialLinkSlice';
import institutionDepartmentReducer from './slices/institutionDepartmentSlice';
import institutionLocationReducer from './slices/institutionLocationSlice';
import institutionAccreditationReducer from './slices/institutionAccreditationSlice';
import institutionRankingReducer from './slices/institutionRankingSlice';
import institutionFacilityReducer from './slices/institutionFacilitySlice';
import courseModuleReducer from './slices/courseModuleSlice';
import courseLessonReducer from './slices/courseLessonSlice';
import coursePrerequisiteReducer from './slices/coursePrerequisiteSlice';
import courseInstructorReducer from './slices/courseInstructorSlice';
import courseReviewReducer from './slices/courseReviewSlice';
import courseAssignmentReducer from './slices/courseAssignmentSlice';
import userCourseProgressReducer from './slices/userCourseProgressSlice';
import userAssignmentSubmissionReducer from './slices/userAssignmentSubmissionSlice';
import jobPostRequirementReducer from './slices/jobPostRequirementSlice';
import jobPostBenefitReducer from './slices/jobPostBenefitSlice';
import jobApplicationReducer from './slices/jobApplicationSlice';
import jobInterviewReducer from './slices/jobInterviewSlice';
import jobPostQuestionReducer from './slices/jobPostQuestionSlice';
import jobApplicationAnswerReducer from './slices/jobApplicationAnswerSlice';
import communityCategoryReducer from './slices/communityCategorySlice';
import communityRuleReducer from './slices/communityRuleSlice';
import communityEventReducer from './slices/communityEventSlice';
import communityEventAttendeeReducer from './slices/communityEventAttendeeSlice';
import postAttachmentReducer from './slices/postAttachmentSlice';
import postTagReducer from './slices/postTagSlice';
import postTagLinkReducer from './slices/postTagLinkSlice';
import marketTrendSkillDemandReducer from './slices/marketTrendSkillDemandSlice';
import marketTrendIndustryReducer from './slices/marketTrendIndustrySlice';
import marketTrendLocationReducer from './slices/marketTrendLocationSlice';
import userSkillEndorsementReducer from './slices/userSkillEndorsementSlice';
import userRecommendationReducer from './slices/userRecommendationSlice';
import notificationReducer from './slices/notificationSlice';
import courseJobPostLinkReducer from './slices/courseJobPostLinkSlice';
import courseCommunityLinkReducer from './slices/courseCommunityLinkSlice';
import jobPostCommunityLinkReducer from './slices/jobPostCommunityLinkSlice';
import marketTrendCourseLinkReducer from './slices/marketTrendCourseLinkSlice';
import marketTrendJobPostLinkReducer from './slices/marketTrendJobPostLinkSlice';
import marketTrendInstitutionLinkReducer from './slices/marketTrendInstitutionLinkSlice';
import userFileReducer from './slices/userFileSlice';
import institutionFileReducer from './slices/institutionFileSlice';
import courseFileReducer from './slices/courseFileSlice';
import jobPostFileReducer from './slices/jobPostFileSlice';
import communityFileReducer from './slices/communityFileSlice';
import marketTrendFileReducer from './slices/marketTrendFileSlice';


export const store = configureStore({
  reducer: {
    user: userReducer,
    userPropertyGroup: userPropertyGroupReducer,
    userProperty: userPropertyReducer,
    institution: institutionReducer,
    institutionPropertyGroup: institutionPropertyGroupReducer,
    institutionProperty: institutionPropertyReducer,
    candidateInstituteLink: candidateInstituteLinkReducer,
    userInstitutePropertyLink: userInstitutePropertyLinkReducer,
    course: courseReducer,
    coursePropertyGroup: coursePropertyGroupReducer,
    courseProperty: coursePropertyReducer,
    userCourseLink: userCourseLinkReducer,
    userCourseWishlist: userCourseWishlistReducer,
    userCoursePurchase: userCoursePurchaseReducer,
    jobPost: jobPostReducer,
    jobPostPropertyGroup: jobPostPropertyGroupReducer,
    jobPostProperty: jobPostPropertyReducer,
    userJobPostBookmark: userJobPostBookmarkReducer,
    jobPostUserBookmark: jobPostUserBookmarkReducer,
    subscriptionPaymentHistory: subscriptionPaymentHistoryReducer,
    community: communityReducer,
    communityPropertyGroup: communityPropertyGroupReducer,
    communityProperty: communityPropertyReducer,
    communityUserLink: communityUserLinkReducer,
    communityPropertyUserLink: communityPropertyUserLinkReducer,
    communityUserPost: communityUserPostReducer,
    communityPostLink: communityPostLinkReducer,
    postEmogi: postEmogiReducer,
    emogiPostUserLink: emogiPostUserLinkReducer,
    postFlag: postFlagReducer,
    postComment: postCommentReducer,
    postCommentEmogiLink: postCommentEmogiLinkReducer,
    aiUserProfileEvaluationParameterGroup: aiUserProfileEvaluationParameterGroupReducer,
    aiUserProfileEvaluationParameter: aiUserProfileEvaluationParameterReducer,
    aiUserProfileEvaluation: aiUserProfileEvaluationReducer,
    aiEvaluationParameterGroup: aiEvaluationParameterGroupReducer,
    aiEvaluationParameter: aiEvaluationParameterReducer,
    aiInstitutionProfileEvaluation: aiInstitutionProfileEvaluationReducer,
    aiJobRecommendation: aiJobRecommendationReducer,
    aiCommunityPostEvaluation: aiCommunityPostEvaluationReducer,
    aiMarketTrendParameterGroup: aiMarketTrendParameterGroupReducer,
    aiMarketTrendParameter: aiMarketTrendParameterReducer,
    aiMarketTrendProperty: aiMarketTrendPropertyReducer,
    userProfileDocument: userProfileDocumentReducer,
    institutionProfileDocument: institutionProfileDocumentReducer,
    courseDocumentGroup: courseDocumentGroupReducer,
    courseDocument: courseDocumentReducer,
    marketTrendDocument: marketTrendDocumentReducer,
    jobPostDocument: jobPostDocumentReducer,
    userEducation: userEducationReducer,
    userWorkExperience: userWorkExperienceReducer,
    userSkill: userSkillReducer,
    userCertification: userCertificationReducer,
    userLanguage: userLanguageReducer,
    userAchievement: userAchievementReducer,
    userSocialLink: userSocialLinkReducer,
    institutionDepartment: institutionDepartmentReducer,
    institutionLocation: institutionLocationReducer,
    institutionAccreditation: institutionAccreditationReducer,
    institutionRanking: institutionRankingReducer,
    institutionFacility: institutionFacilityReducer,
    courseModule: courseModuleReducer,
    courseLesson: courseLessonReducer,
    coursePrerequisite: coursePrerequisiteReducer,
    courseInstructor: courseInstructorReducer,
    courseReview: courseReviewReducer,
    courseAssignment: courseAssignmentReducer,
    userCourseProgress: userCourseProgressReducer,
    userAssignmentSubmission: userAssignmentSubmissionReducer,
    jobPostRequirement: jobPostRequirementReducer,
    jobPostBenefit: jobPostBenefitReducer,
    jobApplication: jobApplicationReducer,
    jobInterview: jobInterviewReducer,
    jobPostQuestion: jobPostQuestionReducer,
    jobApplicationAnswer: jobApplicationAnswerReducer,
    communityCategory: communityCategoryReducer,
    communityRule: communityRuleReducer,
    communityEvent: communityEventReducer,
    communityEventAttendee: communityEventAttendeeReducer,
    postAttachment: postAttachmentReducer,
    postTag: postTagReducer,
    postTagLink: postTagLinkReducer,
    marketTrendSkillDemand: marketTrendSkillDemandReducer,
    marketTrendIndustry: marketTrendIndustryReducer,
    marketTrendLocation: marketTrendLocationReducer,
    userSkillEndorsement: userSkillEndorsementReducer,
    userRecommendation: userRecommendationReducer,
    notification: notificationReducer,
    courseJobPostLink: courseJobPostLinkReducer,
    courseCommunityLink: courseCommunityLinkReducer,
    jobPostCommunityLink: jobPostCommunityLinkReducer,
    marketTrendCourseLink: marketTrendCourseLinkReducer,
    marketTrendJobPostLink: marketTrendJobPostLinkReducer,
    marketTrendInstitutionLink: marketTrendInstitutionLinkReducer,
    userFile: userFileReducer,
    institutionFile: institutionFileReducer,
    courseFile: courseFileReducer,
    jobPostFile: jobPostFileReducer,
    communityFile: communityFileReducer,
    marketTrendFile: marketTrendFileReducer,
  },
});
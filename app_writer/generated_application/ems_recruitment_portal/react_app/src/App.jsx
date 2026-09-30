import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './auth/ProtectedRoute';
import LoginPage from './auth/LoginPage';
import RegisterPage from './auth/RegisterPage';
import AppLayout from './layout/AppLayout';
import UserPage from './pages/entitys/UserPage';
import UserPropertyGroupPage from './pages/entitys/UserPropertyGroupPage';
import UserPropertyPage from './pages/entitys/UserPropertyPage';
import InstitutionPage from './pages/entitys/InstitutionPage';
import InstitutionPropertyGroupPage from './pages/entitys/InstitutionPropertyGroupPage';
import InstitutionPropertyPage from './pages/entitys/InstitutionPropertyPage';
import CandidateInstituteLinkPage from './pages/entitys/CandidateInstituteLinkPage';
import UserInstitutePropertyLinkPage from './pages/entitys/UserInstitutePropertyLinkPage';
import CoursePage from './pages/entitys/CoursePage';
import CoursePropertyGroupPage from './pages/entitys/CoursePropertyGroupPage';
import CoursePropertyPage from './pages/entitys/CoursePropertyPage';
import UserCourseLinkPage from './pages/entitys/UserCourseLinkPage';
import UserCourseWishlistPage from './pages/entitys/UserCourseWishlistPage';
import UserCoursePurchasePage from './pages/entitys/UserCoursePurchasePage';
import JobPostPage from './pages/entitys/JobPostPage';
import JobPostPropertyGroupPage from './pages/entitys/JobPostPropertyGroupPage';
import JobPostPropertyPage from './pages/entitys/JobPostPropertyPage';
import UserJobPostBookmarkPage from './pages/entitys/UserJobPostBookmarkPage';
import JobPostUserBookmarkPage from './pages/entitys/JobPostUserBookmarkPage';
import SubscriptionPaymentHistoryPage from './pages/entitys/SubscriptionPaymentHistoryPage';
import CommunityPage from './pages/entitys/CommunityPage';
import CommunityPropertyGroupPage from './pages/entitys/CommunityPropertyGroupPage';
import CommunityPropertyPage from './pages/entitys/CommunityPropertyPage';
import CommunityUserLinkPage from './pages/entitys/CommunityUserLinkPage';
import CommunityPropertyUserLinkPage from './pages/entitys/CommunityPropertyUserLinkPage';
import CommunityUserPostPage from './pages/entitys/CommunityUserPostPage';
import CommunityPostLinkPage from './pages/entitys/CommunityPostLinkPage';
import PostEmogiPage from './pages/entitys/PostEmogiPage';
import EmogiPostUserLinkPage from './pages/entitys/EmogiPostUserLinkPage';
import PostFlagPage from './pages/entitys/PostFlagPage';
import PostCommentPage from './pages/entitys/PostCommentPage';
import PostCommentEmogiLinkPage from './pages/entitys/PostCommentEmogiLinkPage';
import AiUserProfileEvaluationParameterGroupPage from './pages/entitys/AiUserProfileEvaluationParameterGroupPage';
import AiUserProfileEvaluationParameterPage from './pages/entitys/AiUserProfileEvaluationParameterPage';
import AiUserProfileEvaluationPage from './pages/entitys/AiUserProfileEvaluationPage';
import AiEvaluationParameterGroupPage from './pages/entitys/AiEvaluationParameterGroupPage';
import AiEvaluationParameterPage from './pages/entitys/AiEvaluationParameterPage';
import AiInstitutionProfileEvaluationPage from './pages/entitys/AiInstitutionProfileEvaluationPage';
import AiJobRecommendationPage from './pages/entitys/AiJobRecommendationPage';
import AiCommunityPostEvaluationPage from './pages/entitys/AiCommunityPostEvaluationPage';
import AiMarketTrendParameterGroupPage from './pages/entitys/AiMarketTrendParameterGroupPage';
import AiMarketTrendParameterPage from './pages/entitys/AiMarketTrendParameterPage';
import AiMarketTrendPropertyPage from './pages/entitys/AiMarketTrendPropertyPage';
import UserProfileDocumentPage from './pages/entitys/UserProfileDocumentPage';
import InstitutionProfileDocumentPage from './pages/entitys/InstitutionProfileDocumentPage';
import CourseDocumentGroupPage from './pages/entitys/CourseDocumentGroupPage';
import CourseDocumentPage from './pages/entitys/CourseDocumentPage';
import MarketTrendDocumentPage from './pages/entitys/MarketTrendDocumentPage';
import JobPostDocumentPage from './pages/entitys/JobPostDocumentPage';
import UserEducationPage from './pages/entitys/UserEducationPage';
import UserWorkExperiencePage from './pages/entitys/UserWorkExperiencePage';
import UserSkillPage from './pages/entitys/UserSkillPage';
import UserCertificationPage from './pages/entitys/UserCertificationPage';
import UserLanguagePage from './pages/entitys/UserLanguagePage';
import UserAchievementPage from './pages/entitys/UserAchievementPage';
import UserSocialLinkPage from './pages/entitys/UserSocialLinkPage';
import InstitutionDepartmentPage from './pages/entitys/InstitutionDepartmentPage';
import InstitutionLocationPage from './pages/entitys/InstitutionLocationPage';
import InstitutionAccreditationPage from './pages/entitys/InstitutionAccreditationPage';
import InstitutionRankingPage from './pages/entitys/InstitutionRankingPage';
import InstitutionFacilityPage from './pages/entitys/InstitutionFacilityPage';
import CourseModulePage from './pages/entitys/CourseModulePage';
import CourseLessonPage from './pages/entitys/CourseLessonPage';
import CoursePrerequisitePage from './pages/entitys/CoursePrerequisitePage';
import CourseInstructorPage from './pages/entitys/CourseInstructorPage';
import CourseReviewPage from './pages/entitys/CourseReviewPage';
import CourseAssignmentPage from './pages/entitys/CourseAssignmentPage';
import UserCourseProgressPage from './pages/entitys/UserCourseProgressPage';
import UserAssignmentSubmissionPage from './pages/entitys/UserAssignmentSubmissionPage';
import JobPostRequirementPage from './pages/entitys/JobPostRequirementPage';
import JobPostBenefitPage from './pages/entitys/JobPostBenefitPage';
import JobApplicationPage from './pages/entitys/JobApplicationPage';
import JobInterviewPage from './pages/entitys/JobInterviewPage';
import JobPostQuestionPage from './pages/entitys/JobPostQuestionPage';
import JobApplicationAnswerPage from './pages/entitys/JobApplicationAnswerPage';
import CommunityCategoryPage from './pages/entitys/CommunityCategoryPage';
import CommunityRulePage from './pages/entitys/CommunityRulePage';
import CommunityEventPage from './pages/entitys/CommunityEventPage';
import CommunityEventAttendeePage from './pages/entitys/CommunityEventAttendeePage';
import PostAttachmentPage from './pages/entitys/PostAttachmentPage';
import PostTagPage from './pages/entitys/PostTagPage';
import PostTagLinkPage from './pages/entitys/PostTagLinkPage';
import MarketTrendSkillDemandPage from './pages/entitys/MarketTrendSkillDemandPage';
import MarketTrendIndustryPage from './pages/entitys/MarketTrendIndustryPage';
import MarketTrendLocationPage from './pages/entitys/MarketTrendLocationPage';
import UserSkillEndorsementPage from './pages/entitys/UserSkillEndorsementPage';
import UserRecommendationPage from './pages/entitys/UserRecommendationPage';
import NotificationPage from './pages/entitys/NotificationPage';
import CourseJobPostLinkPage from './pages/entitys/CourseJobPostLinkPage';
import CourseCommunityLinkPage from './pages/entitys/CourseCommunityLinkPage';
import JobPostCommunityLinkPage from './pages/entitys/JobPostCommunityLinkPage';
import MarketTrendCourseLinkPage from './pages/entitys/MarketTrendCourseLinkPage';
import MarketTrendJobPostLinkPage from './pages/entitys/MarketTrendJobPostLinkPage';
import MarketTrendInstitutionLinkPage from './pages/entitys/MarketTrendInstitutionLinkPage';
import UserFilePage from './pages/entitys/UserFilePage';
import InstitutionFilePage from './pages/entitys/InstitutionFilePage';
import CourseFilePage from './pages/entitys/CourseFilePage';
import JobPostFilePage from './pages/entitys/JobPostFilePage';
import CommunityFilePage from './pages/entitys/CommunityFilePage';
import MarketTrendFilePage from './pages/entitys/MarketTrendFilePage';
import UserFilterPage from './pages/filters/UserFilterPage';
import UserPropertyGroupFilterPage from './pages/filters/UserPropertyGroupFilterPage';
import UserPropertyFilterPage from './pages/filters/UserPropertyFilterPage';
import InstitutionFilterPage from './pages/filters/InstitutionFilterPage';
import InstitutionPropertyGroupFilterPage from './pages/filters/InstitutionPropertyGroupFilterPage';
import InstitutionPropertyFilterPage from './pages/filters/InstitutionPropertyFilterPage';
import CandidateInstituteLinkFilterPage from './pages/filters/CandidateInstituteLinkFilterPage';
import UserInstitutePropertyLinkFilterPage from './pages/filters/UserInstitutePropertyLinkFilterPage';
import CourseFilterPage from './pages/filters/CourseFilterPage';
import CoursePropertyGroupFilterPage from './pages/filters/CoursePropertyGroupFilterPage';
import CoursePropertyFilterPage from './pages/filters/CoursePropertyFilterPage';
import UserCourseLinkFilterPage from './pages/filters/UserCourseLinkFilterPage';
import UserCourseWishlistFilterPage from './pages/filters/UserCourseWishlistFilterPage';
import UserCoursePurchaseFilterPage from './pages/filters/UserCoursePurchaseFilterPage';
import JobPostFilterPage from './pages/filters/JobPostFilterPage';
import JobPostPropertyGroupFilterPage from './pages/filters/JobPostPropertyGroupFilterPage';
import JobPostPropertyFilterPage from './pages/filters/JobPostPropertyFilterPage';
import UserJobPostBookmarkFilterPage from './pages/filters/UserJobPostBookmarkFilterPage';
import JobPostUserBookmarkFilterPage from './pages/filters/JobPostUserBookmarkFilterPage';
import SubscriptionPaymentHistoryFilterPage from './pages/filters/SubscriptionPaymentHistoryFilterPage';
import CommunityFilterPage from './pages/filters/CommunityFilterPage';
import CommunityPropertyGroupFilterPage from './pages/filters/CommunityPropertyGroupFilterPage';
import CommunityPropertyFilterPage from './pages/filters/CommunityPropertyFilterPage';
import CommunityUserLinkFilterPage from './pages/filters/CommunityUserLinkFilterPage';
import CommunityPropertyUserLinkFilterPage from './pages/filters/CommunityPropertyUserLinkFilterPage';
import CommunityUserPostFilterPage from './pages/filters/CommunityUserPostFilterPage';
import CommunityPostLinkFilterPage from './pages/filters/CommunityPostLinkFilterPage';
import PostEmogiFilterPage from './pages/filters/PostEmogiFilterPage';
import EmogiPostUserLinkFilterPage from './pages/filters/EmogiPostUserLinkFilterPage';
import PostFlagFilterPage from './pages/filters/PostFlagFilterPage';
import PostCommentFilterPage from './pages/filters/PostCommentFilterPage';
import PostCommentEmogiLinkFilterPage from './pages/filters/PostCommentEmogiLinkFilterPage';
import AiUserProfileEvaluationParameterGroupFilterPage from './pages/filters/AiUserProfileEvaluationParameterGroupFilterPage';
import AiUserProfileEvaluationParameterFilterPage from './pages/filters/AiUserProfileEvaluationParameterFilterPage';
import AiUserProfileEvaluationFilterPage from './pages/filters/AiUserProfileEvaluationFilterPage';
import AiEvaluationParameterGroupFilterPage from './pages/filters/AiEvaluationParameterGroupFilterPage';
import AiEvaluationParameterFilterPage from './pages/filters/AiEvaluationParameterFilterPage';
import AiInstitutionProfileEvaluationFilterPage from './pages/filters/AiInstitutionProfileEvaluationFilterPage';
import AiJobRecommendationFilterPage from './pages/filters/AiJobRecommendationFilterPage';
import AiCommunityPostEvaluationFilterPage from './pages/filters/AiCommunityPostEvaluationFilterPage';
import AiMarketTrendParameterGroupFilterPage from './pages/filters/AiMarketTrendParameterGroupFilterPage';
import AiMarketTrendParameterFilterPage from './pages/filters/AiMarketTrendParameterFilterPage';
import AiMarketTrendPropertyFilterPage from './pages/filters/AiMarketTrendPropertyFilterPage';
import UserProfileDocumentFilterPage from './pages/filters/UserProfileDocumentFilterPage';
import InstitutionProfileDocumentFilterPage from './pages/filters/InstitutionProfileDocumentFilterPage';
import CourseDocumentGroupFilterPage from './pages/filters/CourseDocumentGroupFilterPage';
import CourseDocumentFilterPage from './pages/filters/CourseDocumentFilterPage';
import MarketTrendDocumentFilterPage from './pages/filters/MarketTrendDocumentFilterPage';
import JobPostDocumentFilterPage from './pages/filters/JobPostDocumentFilterPage';
import UserEducationFilterPage from './pages/filters/UserEducationFilterPage';
import UserWorkExperienceFilterPage from './pages/filters/UserWorkExperienceFilterPage';
import UserSkillFilterPage from './pages/filters/UserSkillFilterPage';
import UserCertificationFilterPage from './pages/filters/UserCertificationFilterPage';
import UserLanguageFilterPage from './pages/filters/UserLanguageFilterPage';
import UserAchievementFilterPage from './pages/filters/UserAchievementFilterPage';
import UserSocialLinkFilterPage from './pages/filters/UserSocialLinkFilterPage';
import InstitutionDepartmentFilterPage from './pages/filters/InstitutionDepartmentFilterPage';
import InstitutionLocationFilterPage from './pages/filters/InstitutionLocationFilterPage';
import InstitutionAccreditationFilterPage from './pages/filters/InstitutionAccreditationFilterPage';
import InstitutionRankingFilterPage from './pages/filters/InstitutionRankingFilterPage';
import InstitutionFacilityFilterPage from './pages/filters/InstitutionFacilityFilterPage';
import CourseModuleFilterPage from './pages/filters/CourseModuleFilterPage';
import CourseLessonFilterPage from './pages/filters/CourseLessonFilterPage';
import CoursePrerequisiteFilterPage from './pages/filters/CoursePrerequisiteFilterPage';
import CourseInstructorFilterPage from './pages/filters/CourseInstructorFilterPage';
import CourseReviewFilterPage from './pages/filters/CourseReviewFilterPage';
import CourseAssignmentFilterPage from './pages/filters/CourseAssignmentFilterPage';
import UserCourseProgressFilterPage from './pages/filters/UserCourseProgressFilterPage';
import UserAssignmentSubmissionFilterPage from './pages/filters/UserAssignmentSubmissionFilterPage';
import JobPostRequirementFilterPage from './pages/filters/JobPostRequirementFilterPage';
import JobPostBenefitFilterPage from './pages/filters/JobPostBenefitFilterPage';
import JobApplicationFilterPage from './pages/filters/JobApplicationFilterPage';
import JobInterviewFilterPage from './pages/filters/JobInterviewFilterPage';
import JobPostQuestionFilterPage from './pages/filters/JobPostQuestionFilterPage';
import JobApplicationAnswerFilterPage from './pages/filters/JobApplicationAnswerFilterPage';
import CommunityCategoryFilterPage from './pages/filters/CommunityCategoryFilterPage';
import CommunityRuleFilterPage from './pages/filters/CommunityRuleFilterPage';
import CommunityEventFilterPage from './pages/filters/CommunityEventFilterPage';
import CommunityEventAttendeeFilterPage from './pages/filters/CommunityEventAttendeeFilterPage';
import PostAttachmentFilterPage from './pages/filters/PostAttachmentFilterPage';
import PostTagFilterPage from './pages/filters/PostTagFilterPage';
import PostTagLinkFilterPage from './pages/filters/PostTagLinkFilterPage';
import MarketTrendSkillDemandFilterPage from './pages/filters/MarketTrendSkillDemandFilterPage';
import MarketTrendIndustryFilterPage from './pages/filters/MarketTrendIndustryFilterPage';
import MarketTrendLocationFilterPage from './pages/filters/MarketTrendLocationFilterPage';
import UserSkillEndorsementFilterPage from './pages/filters/UserSkillEndorsementFilterPage';
import UserRecommendationFilterPage from './pages/filters/UserRecommendationFilterPage';
import NotificationFilterPage from './pages/filters/NotificationFilterPage';
import CourseJobPostLinkFilterPage from './pages/filters/CourseJobPostLinkFilterPage';
import CourseCommunityLinkFilterPage from './pages/filters/CourseCommunityLinkFilterPage';
import JobPostCommunityLinkFilterPage from './pages/filters/JobPostCommunityLinkFilterPage';
import MarketTrendCourseLinkFilterPage from './pages/filters/MarketTrendCourseLinkFilterPage';
import MarketTrendJobPostLinkFilterPage from './pages/filters/MarketTrendJobPostLinkFilterPage';
import MarketTrendInstitutionLinkFilterPage from './pages/filters/MarketTrendInstitutionLinkFilterPage';
import UserFileFilterPage from './pages/filters/UserFileFilterPage';
import InstitutionFileFilterPage from './pages/filters/InstitutionFileFilterPage';
import CourseFileFilterPage from './pages/filters/CourseFileFilterPage';
import JobPostFileFilterPage from './pages/filters/JobPostFileFilterPage';
import CommunityFileFilterPage from './pages/filters/CommunityFileFilterPage';
import MarketTrendFileFilterPage from './pages/filters/MarketTrendFileFilterPage';
import UserQueryPage from './pages/queries/UserQueryPage';
import UserPropertyGroupQueryPage from './pages/queries/UserPropertyGroupQueryPage';
import UserPropertyQueryPage from './pages/queries/UserPropertyQueryPage';
import InstitutionQueryPage from './pages/queries/InstitutionQueryPage';
import InstitutionPropertyGroupQueryPage from './pages/queries/InstitutionPropertyGroupQueryPage';
import InstitutionPropertyQueryPage from './pages/queries/InstitutionPropertyQueryPage';
import CandidateInstituteLinkQueryPage from './pages/queries/CandidateInstituteLinkQueryPage';
import UserInstitutePropertyLinkQueryPage from './pages/queries/UserInstitutePropertyLinkQueryPage';
import CourseQueryPage from './pages/queries/CourseQueryPage';
import CoursePropertyGroupQueryPage from './pages/queries/CoursePropertyGroupQueryPage';
import CoursePropertyQueryPage from './pages/queries/CoursePropertyQueryPage';
import UserCourseLinkQueryPage from './pages/queries/UserCourseLinkQueryPage';
import UserCourseWishlistQueryPage from './pages/queries/UserCourseWishlistQueryPage';
import UserCoursePurchaseQueryPage from './pages/queries/UserCoursePurchaseQueryPage';
import JobPostQueryPage from './pages/queries/JobPostQueryPage';
import JobPostPropertyGroupQueryPage from './pages/queries/JobPostPropertyGroupQueryPage';
import JobPostPropertyQueryPage from './pages/queries/JobPostPropertyQueryPage';
import UserJobPostBookmarkQueryPage from './pages/queries/UserJobPostBookmarkQueryPage';
import JobPostUserBookmarkQueryPage from './pages/queries/JobPostUserBookmarkQueryPage';
import SubscriptionPaymentHistoryQueryPage from './pages/queries/SubscriptionPaymentHistoryQueryPage';
import CommunityQueryPage from './pages/queries/CommunityQueryPage';
import CommunityPropertyGroupQueryPage from './pages/queries/CommunityPropertyGroupQueryPage';
import CommunityPropertyQueryPage from './pages/queries/CommunityPropertyQueryPage';
import CommunityUserLinkQueryPage from './pages/queries/CommunityUserLinkQueryPage';
import CommunityPropertyUserLinkQueryPage from './pages/queries/CommunityPropertyUserLinkQueryPage';
import CommunityUserPostQueryPage from './pages/queries/CommunityUserPostQueryPage';
import CommunityPostLinkQueryPage from './pages/queries/CommunityPostLinkQueryPage';
import PostEmogiQueryPage from './pages/queries/PostEmogiQueryPage';
import EmogiPostUserLinkQueryPage from './pages/queries/EmogiPostUserLinkQueryPage';
import PostFlagQueryPage from './pages/queries/PostFlagQueryPage';
import PostCommentQueryPage from './pages/queries/PostCommentQueryPage';
import PostCommentEmogiLinkQueryPage from './pages/queries/PostCommentEmogiLinkQueryPage';
import AiUserProfileEvaluationParameterGroupQueryPage from './pages/queries/AiUserProfileEvaluationParameterGroupQueryPage';
import AiUserProfileEvaluationParameterQueryPage from './pages/queries/AiUserProfileEvaluationParameterQueryPage';
import AiUserProfileEvaluationQueryPage from './pages/queries/AiUserProfileEvaluationQueryPage';
import AiEvaluationParameterGroupQueryPage from './pages/queries/AiEvaluationParameterGroupQueryPage';
import AiEvaluationParameterQueryPage from './pages/queries/AiEvaluationParameterQueryPage';
import AiInstitutionProfileEvaluationQueryPage from './pages/queries/AiInstitutionProfileEvaluationQueryPage';
import AiJobRecommendationQueryPage from './pages/queries/AiJobRecommendationQueryPage';
import AiCommunityPostEvaluationQueryPage from './pages/queries/AiCommunityPostEvaluationQueryPage';
import AiMarketTrendParameterGroupQueryPage from './pages/queries/AiMarketTrendParameterGroupQueryPage';
import AiMarketTrendParameterQueryPage from './pages/queries/AiMarketTrendParameterQueryPage';
import AiMarketTrendPropertyQueryPage from './pages/queries/AiMarketTrendPropertyQueryPage';
import UserProfileDocumentQueryPage from './pages/queries/UserProfileDocumentQueryPage';
import InstitutionProfileDocumentQueryPage from './pages/queries/InstitutionProfileDocumentQueryPage';
import CourseDocumentGroupQueryPage from './pages/queries/CourseDocumentGroupQueryPage';
import CourseDocumentQueryPage from './pages/queries/CourseDocumentQueryPage';
import MarketTrendDocumentQueryPage from './pages/queries/MarketTrendDocumentQueryPage';
import JobPostDocumentQueryPage from './pages/queries/JobPostDocumentQueryPage';
import UserEducationQueryPage from './pages/queries/UserEducationQueryPage';
import UserWorkExperienceQueryPage from './pages/queries/UserWorkExperienceQueryPage';
import UserSkillQueryPage from './pages/queries/UserSkillQueryPage';
import UserCertificationQueryPage from './pages/queries/UserCertificationQueryPage';
import UserLanguageQueryPage from './pages/queries/UserLanguageQueryPage';
import UserAchievementQueryPage from './pages/queries/UserAchievementQueryPage';
import UserSocialLinkQueryPage from './pages/queries/UserSocialLinkQueryPage';
import InstitutionDepartmentQueryPage from './pages/queries/InstitutionDepartmentQueryPage';
import InstitutionLocationQueryPage from './pages/queries/InstitutionLocationQueryPage';
import InstitutionAccreditationQueryPage from './pages/queries/InstitutionAccreditationQueryPage';
import InstitutionRankingQueryPage from './pages/queries/InstitutionRankingQueryPage';
import InstitutionFacilityQueryPage from './pages/queries/InstitutionFacilityQueryPage';
import CourseModuleQueryPage from './pages/queries/CourseModuleQueryPage';
import CourseLessonQueryPage from './pages/queries/CourseLessonQueryPage';
import CoursePrerequisiteQueryPage from './pages/queries/CoursePrerequisiteQueryPage';
import CourseInstructorQueryPage from './pages/queries/CourseInstructorQueryPage';
import CourseReviewQueryPage from './pages/queries/CourseReviewQueryPage';
import CourseAssignmentQueryPage from './pages/queries/CourseAssignmentQueryPage';
import UserCourseProgressQueryPage from './pages/queries/UserCourseProgressQueryPage';
import UserAssignmentSubmissionQueryPage from './pages/queries/UserAssignmentSubmissionQueryPage';
import JobPostRequirementQueryPage from './pages/queries/JobPostRequirementQueryPage';
import JobPostBenefitQueryPage from './pages/queries/JobPostBenefitQueryPage';
import JobApplicationQueryPage from './pages/queries/JobApplicationQueryPage';
import JobInterviewQueryPage from './pages/queries/JobInterviewQueryPage';
import JobPostQuestionQueryPage from './pages/queries/JobPostQuestionQueryPage';
import JobApplicationAnswerQueryPage from './pages/queries/JobApplicationAnswerQueryPage';
import CommunityCategoryQueryPage from './pages/queries/CommunityCategoryQueryPage';
import CommunityRuleQueryPage from './pages/queries/CommunityRuleQueryPage';
import CommunityEventQueryPage from './pages/queries/CommunityEventQueryPage';
import CommunityEventAttendeeQueryPage from './pages/queries/CommunityEventAttendeeQueryPage';
import PostAttachmentQueryPage from './pages/queries/PostAttachmentQueryPage';
import PostTagQueryPage from './pages/queries/PostTagQueryPage';
import PostTagLinkQueryPage from './pages/queries/PostTagLinkQueryPage';
import MarketTrendSkillDemandQueryPage from './pages/queries/MarketTrendSkillDemandQueryPage';
import MarketTrendIndustryQueryPage from './pages/queries/MarketTrendIndustryQueryPage';
import MarketTrendLocationQueryPage from './pages/queries/MarketTrendLocationQueryPage';
import UserSkillEndorsementQueryPage from './pages/queries/UserSkillEndorsementQueryPage';
import UserRecommendationQueryPage from './pages/queries/UserRecommendationQueryPage';
import NotificationQueryPage from './pages/queries/NotificationQueryPage';
import CourseJobPostLinkQueryPage from './pages/queries/CourseJobPostLinkQueryPage';
import CourseCommunityLinkQueryPage from './pages/queries/CourseCommunityLinkQueryPage';
import JobPostCommunityLinkQueryPage from './pages/queries/JobPostCommunityLinkQueryPage';
import MarketTrendCourseLinkQueryPage from './pages/queries/MarketTrendCourseLinkQueryPage';
import MarketTrendJobPostLinkQueryPage from './pages/queries/MarketTrendJobPostLinkQueryPage';
import MarketTrendInstitutionLinkQueryPage from './pages/queries/MarketTrendInstitutionLinkQueryPage';
import UserFileQueryPage from './pages/queries/UserFileQueryPage';
import InstitutionFileQueryPage from './pages/queries/InstitutionFileQueryPage';
import CourseFileQueryPage from './pages/queries/CourseFileQueryPage';
import JobPostFileQueryPage from './pages/queries/JobPostFileQueryPage';
import CommunityFileQueryPage from './pages/queries/CommunityFileQueryPage';
import MarketTrendFileQueryPage from './pages/queries/MarketTrendFileQueryPage';


function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route element={<AppLayout />}>
        <Route path="/user" element={<ProtectedRoute><UserPage /></ProtectedRoute>} />
        <Route path="/user-property-group" element={<ProtectedRoute><UserPropertyGroupPage /></ProtectedRoute>} />
        <Route path="/user-property" element={<ProtectedRoute><UserPropertyPage /></ProtectedRoute>} />
        <Route path="/institution" element={<ProtectedRoute><InstitutionPage /></ProtectedRoute>} />
        <Route path="/institution-property-group" element={<ProtectedRoute><InstitutionPropertyGroupPage /></ProtectedRoute>} />
        <Route path="/institution-property" element={<ProtectedRoute><InstitutionPropertyPage /></ProtectedRoute>} />
        <Route path="/candidate-institute-link" element={<ProtectedRoute><CandidateInstituteLinkPage /></ProtectedRoute>} />
        <Route path="/user-institute-property-link" element={<ProtectedRoute><UserInstitutePropertyLinkPage /></ProtectedRoute>} />
        <Route path="/course" element={<ProtectedRoute><CoursePage /></ProtectedRoute>} />
        <Route path="/course-property-group" element={<ProtectedRoute><CoursePropertyGroupPage /></ProtectedRoute>} />
        <Route path="/course-property" element={<ProtectedRoute><CoursePropertyPage /></ProtectedRoute>} />
        <Route path="/user-course-link" element={<ProtectedRoute><UserCourseLinkPage /></ProtectedRoute>} />
        <Route path="/user-course-wishlist" element={<ProtectedRoute><UserCourseWishlistPage /></ProtectedRoute>} />
        <Route path="/user-course-purchase" element={<ProtectedRoute><UserCoursePurchasePage /></ProtectedRoute>} />
        <Route path="/job-post" element={<ProtectedRoute><JobPostPage /></ProtectedRoute>} />
        <Route path="/job-post-property-group" element={<ProtectedRoute><JobPostPropertyGroupPage /></ProtectedRoute>} />
        <Route path="/job-post-property" element={<ProtectedRoute><JobPostPropertyPage /></ProtectedRoute>} />
        <Route path="/user-job-post-bookmark" element={<ProtectedRoute><UserJobPostBookmarkPage /></ProtectedRoute>} />
        <Route path="/job-post-user-bookmark" element={<ProtectedRoute><JobPostUserBookmarkPage /></ProtectedRoute>} />
        <Route path="/subscription-payment-history" element={<ProtectedRoute><SubscriptionPaymentHistoryPage /></ProtectedRoute>} />
        <Route path="/community" element={<ProtectedRoute><CommunityPage /></ProtectedRoute>} />
        <Route path="/community-property-group" element={<ProtectedRoute><CommunityPropertyGroupPage /></ProtectedRoute>} />
        <Route path="/community-property" element={<ProtectedRoute><CommunityPropertyPage /></ProtectedRoute>} />
        <Route path="/community-user-link" element={<ProtectedRoute><CommunityUserLinkPage /></ProtectedRoute>} />
        <Route path="/community-property-user-link" element={<ProtectedRoute><CommunityPropertyUserLinkPage /></ProtectedRoute>} />
        <Route path="/community-user-post" element={<ProtectedRoute><CommunityUserPostPage /></ProtectedRoute>} />
        <Route path="/community-post-link" element={<ProtectedRoute><CommunityPostLinkPage /></ProtectedRoute>} />
        <Route path="/post-emogi" element={<ProtectedRoute><PostEmogiPage /></ProtectedRoute>} />
        <Route path="/emogi-post-user-link" element={<ProtectedRoute><EmogiPostUserLinkPage /></ProtectedRoute>} />
        <Route path="/post-flag" element={<ProtectedRoute><PostFlagPage /></ProtectedRoute>} />
        <Route path="/post-comment" element={<ProtectedRoute><PostCommentPage /></ProtectedRoute>} />
        <Route path="/post-comment-emogi-link" element={<ProtectedRoute><PostCommentEmogiLinkPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter-group" element={<ProtectedRoute><AiUserProfileEvaluationParameterGroupPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter" element={<ProtectedRoute><AiUserProfileEvaluationParameterPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation" element={<ProtectedRoute><AiUserProfileEvaluationPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter-group" element={<ProtectedRoute><AiEvaluationParameterGroupPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter" element={<ProtectedRoute><AiEvaluationParameterPage /></ProtectedRoute>} />
        <Route path="/ai-institution-profile-evaluation" element={<ProtectedRoute><AiInstitutionProfileEvaluationPage /></ProtectedRoute>} />
        <Route path="/ai-job-recommendation" element={<ProtectedRoute><AiJobRecommendationPage /></ProtectedRoute>} />
        <Route path="/ai-community-post-evaluation" element={<ProtectedRoute><AiCommunityPostEvaluationPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter-group" element={<ProtectedRoute><AiMarketTrendParameterGroupPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter" element={<ProtectedRoute><AiMarketTrendParameterPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-property" element={<ProtectedRoute><AiMarketTrendPropertyPage /></ProtectedRoute>} />
        <Route path="/user-profile-document" element={<ProtectedRoute><UserProfileDocumentPage /></ProtectedRoute>} />
        <Route path="/institution-profile-document" element={<ProtectedRoute><InstitutionProfileDocumentPage /></ProtectedRoute>} />
        <Route path="/course-document-group" element={<ProtectedRoute><CourseDocumentGroupPage /></ProtectedRoute>} />
        <Route path="/course-document" element={<ProtectedRoute><CourseDocumentPage /></ProtectedRoute>} />
        <Route path="/market-trend-document" element={<ProtectedRoute><MarketTrendDocumentPage /></ProtectedRoute>} />
        <Route path="/job-post-document" element={<ProtectedRoute><JobPostDocumentPage /></ProtectedRoute>} />
        <Route path="/user-education" element={<ProtectedRoute><UserEducationPage /></ProtectedRoute>} />
        <Route path="/user-work-experience" element={<ProtectedRoute><UserWorkExperiencePage /></ProtectedRoute>} />
        <Route path="/user-skill" element={<ProtectedRoute><UserSkillPage /></ProtectedRoute>} />
        <Route path="/user-certification" element={<ProtectedRoute><UserCertificationPage /></ProtectedRoute>} />
        <Route path="/user-language" element={<ProtectedRoute><UserLanguagePage /></ProtectedRoute>} />
        <Route path="/user-achievement" element={<ProtectedRoute><UserAchievementPage /></ProtectedRoute>} />
        <Route path="/user-social-link" element={<ProtectedRoute><UserSocialLinkPage /></ProtectedRoute>} />
        <Route path="/institution-department" element={<ProtectedRoute><InstitutionDepartmentPage /></ProtectedRoute>} />
        <Route path="/institution-location" element={<ProtectedRoute><InstitutionLocationPage /></ProtectedRoute>} />
        <Route path="/institution-accreditation" element={<ProtectedRoute><InstitutionAccreditationPage /></ProtectedRoute>} />
        <Route path="/institution-ranking" element={<ProtectedRoute><InstitutionRankingPage /></ProtectedRoute>} />
        <Route path="/institution-facility" element={<ProtectedRoute><InstitutionFacilityPage /></ProtectedRoute>} />
        <Route path="/course-module" element={<ProtectedRoute><CourseModulePage /></ProtectedRoute>} />
        <Route path="/course-lesson" element={<ProtectedRoute><CourseLessonPage /></ProtectedRoute>} />
        <Route path="/course-prerequisite" element={<ProtectedRoute><CoursePrerequisitePage /></ProtectedRoute>} />
        <Route path="/course-instructor" element={<ProtectedRoute><CourseInstructorPage /></ProtectedRoute>} />
        <Route path="/course-review" element={<ProtectedRoute><CourseReviewPage /></ProtectedRoute>} />
        <Route path="/course-assignment" element={<ProtectedRoute><CourseAssignmentPage /></ProtectedRoute>} />
        <Route path="/user-course-progress" element={<ProtectedRoute><UserCourseProgressPage /></ProtectedRoute>} />
        <Route path="/user-assignment-submission" element={<ProtectedRoute><UserAssignmentSubmissionPage /></ProtectedRoute>} />
        <Route path="/job-post-requirement" element={<ProtectedRoute><JobPostRequirementPage /></ProtectedRoute>} />
        <Route path="/job-post-benefit" element={<ProtectedRoute><JobPostBenefitPage /></ProtectedRoute>} />
        <Route path="/job-application" element={<ProtectedRoute><JobApplicationPage /></ProtectedRoute>} />
        <Route path="/job-interview" element={<ProtectedRoute><JobInterviewPage /></ProtectedRoute>} />
        <Route path="/job-post-question" element={<ProtectedRoute><JobPostQuestionPage /></ProtectedRoute>} />
        <Route path="/job-application-answer" element={<ProtectedRoute><JobApplicationAnswerPage /></ProtectedRoute>} />
        <Route path="/community-category" element={<ProtectedRoute><CommunityCategoryPage /></ProtectedRoute>} />
        <Route path="/community-rule" element={<ProtectedRoute><CommunityRulePage /></ProtectedRoute>} />
        <Route path="/community-event" element={<ProtectedRoute><CommunityEventPage /></ProtectedRoute>} />
        <Route path="/community-event-attendee" element={<ProtectedRoute><CommunityEventAttendeePage /></ProtectedRoute>} />
        <Route path="/post-attachment" element={<ProtectedRoute><PostAttachmentPage /></ProtectedRoute>} />
        <Route path="/post-tag" element={<ProtectedRoute><PostTagPage /></ProtectedRoute>} />
        <Route path="/post-tag-link" element={<ProtectedRoute><PostTagLinkPage /></ProtectedRoute>} />
        <Route path="/market-trend-skill-demand" element={<ProtectedRoute><MarketTrendSkillDemandPage /></ProtectedRoute>} />
        <Route path="/market-trend-industry" element={<ProtectedRoute><MarketTrendIndustryPage /></ProtectedRoute>} />
        <Route path="/market-trend-location" element={<ProtectedRoute><MarketTrendLocationPage /></ProtectedRoute>} />
        <Route path="/user-skill-endorsement" element={<ProtectedRoute><UserSkillEndorsementPage /></ProtectedRoute>} />
        <Route path="/user-recommendation" element={<ProtectedRoute><UserRecommendationPage /></ProtectedRoute>} />
        <Route path="/notification" element={<ProtectedRoute><NotificationPage /></ProtectedRoute>} />
        <Route path="/course-job-post-link" element={<ProtectedRoute><CourseJobPostLinkPage /></ProtectedRoute>} />
        <Route path="/course-community-link" element={<ProtectedRoute><CourseCommunityLinkPage /></ProtectedRoute>} />
        <Route path="/job-post-community-link" element={<ProtectedRoute><JobPostCommunityLinkPage /></ProtectedRoute>} />
        <Route path="/market-trend-course-link" element={<ProtectedRoute><MarketTrendCourseLinkPage /></ProtectedRoute>} />
        <Route path="/market-trend-job-post-link" element={<ProtectedRoute><MarketTrendJobPostLinkPage /></ProtectedRoute>} />
        <Route path="/market-trend-institution-link" element={<ProtectedRoute><MarketTrendInstitutionLinkPage /></ProtectedRoute>} />
        <Route path="/user-file" element={<ProtectedRoute><UserFilePage /></ProtectedRoute>} />
        <Route path="/institution-file" element={<ProtectedRoute><InstitutionFilePage /></ProtectedRoute>} />
        <Route path="/course-file" element={<ProtectedRoute><CourseFilePage /></ProtectedRoute>} />
        <Route path="/job-post-file" element={<ProtectedRoute><JobPostFilePage /></ProtectedRoute>} />
        <Route path="/community-file" element={<ProtectedRoute><CommunityFilePage /></ProtectedRoute>} />
        <Route path="/market-trend-file" element={<ProtectedRoute><MarketTrendFilePage /></ProtectedRoute>} />
        <Route path="/user/filter" element={<ProtectedRoute><UserFilterPage /></ProtectedRoute>} />
        <Route path="/user-property-group/filter" element={<ProtectedRoute><UserPropertyGroupFilterPage /></ProtectedRoute>} />
        <Route path="/user-property/filter" element={<ProtectedRoute><UserPropertyFilterPage /></ProtectedRoute>} />
        <Route path="/institution/filter" element={<ProtectedRoute><InstitutionFilterPage /></ProtectedRoute>} />
        <Route path="/institution-property-group/filter" element={<ProtectedRoute><InstitutionPropertyGroupFilterPage /></ProtectedRoute>} />
        <Route path="/institution-property/filter" element={<ProtectedRoute><InstitutionPropertyFilterPage /></ProtectedRoute>} />
        <Route path="/candidate-institute-link/filter" element={<ProtectedRoute><CandidateInstituteLinkFilterPage /></ProtectedRoute>} />
        <Route path="/user-institute-property-link/filter" element={<ProtectedRoute><UserInstitutePropertyLinkFilterPage /></ProtectedRoute>} />
        <Route path="/course/filter" element={<ProtectedRoute><CourseFilterPage /></ProtectedRoute>} />
        <Route path="/course-property-group/filter" element={<ProtectedRoute><CoursePropertyGroupFilterPage /></ProtectedRoute>} />
        <Route path="/course-property/filter" element={<ProtectedRoute><CoursePropertyFilterPage /></ProtectedRoute>} />
        <Route path="/user-course-link/filter" element={<ProtectedRoute><UserCourseLinkFilterPage /></ProtectedRoute>} />
        <Route path="/user-course-wishlist/filter" element={<ProtectedRoute><UserCourseWishlistFilterPage /></ProtectedRoute>} />
        <Route path="/user-course-purchase/filter" element={<ProtectedRoute><UserCoursePurchaseFilterPage /></ProtectedRoute>} />
        <Route path="/job-post/filter" element={<ProtectedRoute><JobPostFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-property-group/filter" element={<ProtectedRoute><JobPostPropertyGroupFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-property/filter" element={<ProtectedRoute><JobPostPropertyFilterPage /></ProtectedRoute>} />
        <Route path="/user-job-post-bookmark/filter" element={<ProtectedRoute><UserJobPostBookmarkFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-user-bookmark/filter" element={<ProtectedRoute><JobPostUserBookmarkFilterPage /></ProtectedRoute>} />
        <Route path="/subscription-payment-history/filter" element={<ProtectedRoute><SubscriptionPaymentHistoryFilterPage /></ProtectedRoute>} />
        <Route path="/community/filter" element={<ProtectedRoute><CommunityFilterPage /></ProtectedRoute>} />
        <Route path="/community-property-group/filter" element={<ProtectedRoute><CommunityPropertyGroupFilterPage /></ProtectedRoute>} />
        <Route path="/community-property/filter" element={<ProtectedRoute><CommunityPropertyFilterPage /></ProtectedRoute>} />
        <Route path="/community-user-link/filter" element={<ProtectedRoute><CommunityUserLinkFilterPage /></ProtectedRoute>} />
        <Route path="/community-property-user-link/filter" element={<ProtectedRoute><CommunityPropertyUserLinkFilterPage /></ProtectedRoute>} />
        <Route path="/community-user-post/filter" element={<ProtectedRoute><CommunityUserPostFilterPage /></ProtectedRoute>} />
        <Route path="/community-post-link/filter" element={<ProtectedRoute><CommunityPostLinkFilterPage /></ProtectedRoute>} />
        <Route path="/post-emogi/filter" element={<ProtectedRoute><PostEmogiFilterPage /></ProtectedRoute>} />
        <Route path="/emogi-post-user-link/filter" element={<ProtectedRoute><EmogiPostUserLinkFilterPage /></ProtectedRoute>} />
        <Route path="/post-flag/filter" element={<ProtectedRoute><PostFlagFilterPage /></ProtectedRoute>} />
        <Route path="/post-comment/filter" element={<ProtectedRoute><PostCommentFilterPage /></ProtectedRoute>} />
        <Route path="/post-comment-emogi-link/filter" element={<ProtectedRoute><PostCommentEmogiLinkFilterPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter-group/filter" element={<ProtectedRoute><AiUserProfileEvaluationParameterGroupFilterPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter/filter" element={<ProtectedRoute><AiUserProfileEvaluationParameterFilterPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation/filter" element={<ProtectedRoute><AiUserProfileEvaluationFilterPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter-group/filter" element={<ProtectedRoute><AiEvaluationParameterGroupFilterPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter/filter" element={<ProtectedRoute><AiEvaluationParameterFilterPage /></ProtectedRoute>} />
        <Route path="/ai-institution-profile-evaluation/filter" element={<ProtectedRoute><AiInstitutionProfileEvaluationFilterPage /></ProtectedRoute>} />
        <Route path="/ai-job-recommendation/filter" element={<ProtectedRoute><AiJobRecommendationFilterPage /></ProtectedRoute>} />
        <Route path="/ai-community-post-evaluation/filter" element={<ProtectedRoute><AiCommunityPostEvaluationFilterPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter-group/filter" element={<ProtectedRoute><AiMarketTrendParameterGroupFilterPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter/filter" element={<ProtectedRoute><AiMarketTrendParameterFilterPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-property/filter" element={<ProtectedRoute><AiMarketTrendPropertyFilterPage /></ProtectedRoute>} />
        <Route path="/user-profile-document/filter" element={<ProtectedRoute><UserProfileDocumentFilterPage /></ProtectedRoute>} />
        <Route path="/institution-profile-document/filter" element={<ProtectedRoute><InstitutionProfileDocumentFilterPage /></ProtectedRoute>} />
        <Route path="/course-document-group/filter" element={<ProtectedRoute><CourseDocumentGroupFilterPage /></ProtectedRoute>} />
        <Route path="/course-document/filter" element={<ProtectedRoute><CourseDocumentFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-document/filter" element={<ProtectedRoute><MarketTrendDocumentFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-document/filter" element={<ProtectedRoute><JobPostDocumentFilterPage /></ProtectedRoute>} />
        <Route path="/user-education/filter" element={<ProtectedRoute><UserEducationFilterPage /></ProtectedRoute>} />
        <Route path="/user-work-experience/filter" element={<ProtectedRoute><UserWorkExperienceFilterPage /></ProtectedRoute>} />
        <Route path="/user-skill/filter" element={<ProtectedRoute><UserSkillFilterPage /></ProtectedRoute>} />
        <Route path="/user-certification/filter" element={<ProtectedRoute><UserCertificationFilterPage /></ProtectedRoute>} />
        <Route path="/user-language/filter" element={<ProtectedRoute><UserLanguageFilterPage /></ProtectedRoute>} />
        <Route path="/user-achievement/filter" element={<ProtectedRoute><UserAchievementFilterPage /></ProtectedRoute>} />
        <Route path="/user-social-link/filter" element={<ProtectedRoute><UserSocialLinkFilterPage /></ProtectedRoute>} />
        <Route path="/institution-department/filter" element={<ProtectedRoute><InstitutionDepartmentFilterPage /></ProtectedRoute>} />
        <Route path="/institution-location/filter" element={<ProtectedRoute><InstitutionLocationFilterPage /></ProtectedRoute>} />
        <Route path="/institution-accreditation/filter" element={<ProtectedRoute><InstitutionAccreditationFilterPage /></ProtectedRoute>} />
        <Route path="/institution-ranking/filter" element={<ProtectedRoute><InstitutionRankingFilterPage /></ProtectedRoute>} />
        <Route path="/institution-facility/filter" element={<ProtectedRoute><InstitutionFacilityFilterPage /></ProtectedRoute>} />
        <Route path="/course-module/filter" element={<ProtectedRoute><CourseModuleFilterPage /></ProtectedRoute>} />
        <Route path="/course-lesson/filter" element={<ProtectedRoute><CourseLessonFilterPage /></ProtectedRoute>} />
        <Route path="/course-prerequisite/filter" element={<ProtectedRoute><CoursePrerequisiteFilterPage /></ProtectedRoute>} />
        <Route path="/course-instructor/filter" element={<ProtectedRoute><CourseInstructorFilterPage /></ProtectedRoute>} />
        <Route path="/course-review/filter" element={<ProtectedRoute><CourseReviewFilterPage /></ProtectedRoute>} />
        <Route path="/course-assignment/filter" element={<ProtectedRoute><CourseAssignmentFilterPage /></ProtectedRoute>} />
        <Route path="/user-course-progress/filter" element={<ProtectedRoute><UserCourseProgressFilterPage /></ProtectedRoute>} />
        <Route path="/user-assignment-submission/filter" element={<ProtectedRoute><UserAssignmentSubmissionFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-requirement/filter" element={<ProtectedRoute><JobPostRequirementFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-benefit/filter" element={<ProtectedRoute><JobPostBenefitFilterPage /></ProtectedRoute>} />
        <Route path="/job-application/filter" element={<ProtectedRoute><JobApplicationFilterPage /></ProtectedRoute>} />
        <Route path="/job-interview/filter" element={<ProtectedRoute><JobInterviewFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-question/filter" element={<ProtectedRoute><JobPostQuestionFilterPage /></ProtectedRoute>} />
        <Route path="/job-application-answer/filter" element={<ProtectedRoute><JobApplicationAnswerFilterPage /></ProtectedRoute>} />
        <Route path="/community-category/filter" element={<ProtectedRoute><CommunityCategoryFilterPage /></ProtectedRoute>} />
        <Route path="/community-rule/filter" element={<ProtectedRoute><CommunityRuleFilterPage /></ProtectedRoute>} />
        <Route path="/community-event/filter" element={<ProtectedRoute><CommunityEventFilterPage /></ProtectedRoute>} />
        <Route path="/community-event-attendee/filter" element={<ProtectedRoute><CommunityEventAttendeeFilterPage /></ProtectedRoute>} />
        <Route path="/post-attachment/filter" element={<ProtectedRoute><PostAttachmentFilterPage /></ProtectedRoute>} />
        <Route path="/post-tag/filter" element={<ProtectedRoute><PostTagFilterPage /></ProtectedRoute>} />
        <Route path="/post-tag-link/filter" element={<ProtectedRoute><PostTagLinkFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-skill-demand/filter" element={<ProtectedRoute><MarketTrendSkillDemandFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-industry/filter" element={<ProtectedRoute><MarketTrendIndustryFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-location/filter" element={<ProtectedRoute><MarketTrendLocationFilterPage /></ProtectedRoute>} />
        <Route path="/user-skill-endorsement/filter" element={<ProtectedRoute><UserSkillEndorsementFilterPage /></ProtectedRoute>} />
        <Route path="/user-recommendation/filter" element={<ProtectedRoute><UserRecommendationFilterPage /></ProtectedRoute>} />
        <Route path="/notification/filter" element={<ProtectedRoute><NotificationFilterPage /></ProtectedRoute>} />
        <Route path="/course-job-post-link/filter" element={<ProtectedRoute><CourseJobPostLinkFilterPage /></ProtectedRoute>} />
        <Route path="/course-community-link/filter" element={<ProtectedRoute><CourseCommunityLinkFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-community-link/filter" element={<ProtectedRoute><JobPostCommunityLinkFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-course-link/filter" element={<ProtectedRoute><MarketTrendCourseLinkFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-job-post-link/filter" element={<ProtectedRoute><MarketTrendJobPostLinkFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-institution-link/filter" element={<ProtectedRoute><MarketTrendInstitutionLinkFilterPage /></ProtectedRoute>} />
        <Route path="/user-file/filter" element={<ProtectedRoute><UserFileFilterPage /></ProtectedRoute>} />
        <Route path="/institution-file/filter" element={<ProtectedRoute><InstitutionFileFilterPage /></ProtectedRoute>} />
        <Route path="/course-file/filter" element={<ProtectedRoute><CourseFileFilterPage /></ProtectedRoute>} />
        <Route path="/job-post-file/filter" element={<ProtectedRoute><JobPostFileFilterPage /></ProtectedRoute>} />
        <Route path="/community-file/filter" element={<ProtectedRoute><CommunityFileFilterPage /></ProtectedRoute>} />
        <Route path="/market-trend-file/filter" element={<ProtectedRoute><MarketTrendFileFilterPage /></ProtectedRoute>} />
        <Route path="/user/queries" element={<ProtectedRoute><UserQueryPage /></ProtectedRoute>} />
        <Route path="/user-property-group/queries" element={<ProtectedRoute><UserPropertyGroupQueryPage /></ProtectedRoute>} />
        <Route path="/user-property/queries" element={<ProtectedRoute><UserPropertyQueryPage /></ProtectedRoute>} />
        <Route path="/institution/queries" element={<ProtectedRoute><InstitutionQueryPage /></ProtectedRoute>} />
        <Route path="/institution-property-group/queries" element={<ProtectedRoute><InstitutionPropertyGroupQueryPage /></ProtectedRoute>} />
        <Route path="/institution-property/queries" element={<ProtectedRoute><InstitutionPropertyQueryPage /></ProtectedRoute>} />
        <Route path="/candidate-institute-link/queries" element={<ProtectedRoute><CandidateInstituteLinkQueryPage /></ProtectedRoute>} />
        <Route path="/user-institute-property-link/queries" element={<ProtectedRoute><UserInstitutePropertyLinkQueryPage /></ProtectedRoute>} />
        <Route path="/course/queries" element={<ProtectedRoute><CourseQueryPage /></ProtectedRoute>} />
        <Route path="/course-property-group/queries" element={<ProtectedRoute><CoursePropertyGroupQueryPage /></ProtectedRoute>} />
        <Route path="/course-property/queries" element={<ProtectedRoute><CoursePropertyQueryPage /></ProtectedRoute>} />
        <Route path="/user-course-link/queries" element={<ProtectedRoute><UserCourseLinkQueryPage /></ProtectedRoute>} />
        <Route path="/user-course-wishlist/queries" element={<ProtectedRoute><UserCourseWishlistQueryPage /></ProtectedRoute>} />
        <Route path="/user-course-purchase/queries" element={<ProtectedRoute><UserCoursePurchaseQueryPage /></ProtectedRoute>} />
        <Route path="/job-post/queries" element={<ProtectedRoute><JobPostQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-property-group/queries" element={<ProtectedRoute><JobPostPropertyGroupQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-property/queries" element={<ProtectedRoute><JobPostPropertyQueryPage /></ProtectedRoute>} />
        <Route path="/user-job-post-bookmark/queries" element={<ProtectedRoute><UserJobPostBookmarkQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-user-bookmark/queries" element={<ProtectedRoute><JobPostUserBookmarkQueryPage /></ProtectedRoute>} />
        <Route path="/subscription-payment-history/queries" element={<ProtectedRoute><SubscriptionPaymentHistoryQueryPage /></ProtectedRoute>} />
        <Route path="/community/queries" element={<ProtectedRoute><CommunityQueryPage /></ProtectedRoute>} />
        <Route path="/community-property-group/queries" element={<ProtectedRoute><CommunityPropertyGroupQueryPage /></ProtectedRoute>} />
        <Route path="/community-property/queries" element={<ProtectedRoute><CommunityPropertyQueryPage /></ProtectedRoute>} />
        <Route path="/community-user-link/queries" element={<ProtectedRoute><CommunityUserLinkQueryPage /></ProtectedRoute>} />
        <Route path="/community-property-user-link/queries" element={<ProtectedRoute><CommunityPropertyUserLinkQueryPage /></ProtectedRoute>} />
        <Route path="/community-user-post/queries" element={<ProtectedRoute><CommunityUserPostQueryPage /></ProtectedRoute>} />
        <Route path="/community-post-link/queries" element={<ProtectedRoute><CommunityPostLinkQueryPage /></ProtectedRoute>} />
        <Route path="/post-emogi/queries" element={<ProtectedRoute><PostEmogiQueryPage /></ProtectedRoute>} />
        <Route path="/emogi-post-user-link/queries" element={<ProtectedRoute><EmogiPostUserLinkQueryPage /></ProtectedRoute>} />
        <Route path="/post-flag/queries" element={<ProtectedRoute><PostFlagQueryPage /></ProtectedRoute>} />
        <Route path="/post-comment/queries" element={<ProtectedRoute><PostCommentQueryPage /></ProtectedRoute>} />
        <Route path="/post-comment-emogi-link/queries" element={<ProtectedRoute><PostCommentEmogiLinkQueryPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter-group/queries" element={<ProtectedRoute><AiUserProfileEvaluationParameterGroupQueryPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation-parameter/queries" element={<ProtectedRoute><AiUserProfileEvaluationParameterQueryPage /></ProtectedRoute>} />
        <Route path="/ai-user-profile-evaluation/queries" element={<ProtectedRoute><AiUserProfileEvaluationQueryPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter-group/queries" element={<ProtectedRoute><AiEvaluationParameterGroupQueryPage /></ProtectedRoute>} />
        <Route path="/ai-evaluation-parameter/queries" element={<ProtectedRoute><AiEvaluationParameterQueryPage /></ProtectedRoute>} />
        <Route path="/ai-institution-profile-evaluation/queries" element={<ProtectedRoute><AiInstitutionProfileEvaluationQueryPage /></ProtectedRoute>} />
        <Route path="/ai-job-recommendation/queries" element={<ProtectedRoute><AiJobRecommendationQueryPage /></ProtectedRoute>} />
        <Route path="/ai-community-post-evaluation/queries" element={<ProtectedRoute><AiCommunityPostEvaluationQueryPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter-group/queries" element={<ProtectedRoute><AiMarketTrendParameterGroupQueryPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-parameter/queries" element={<ProtectedRoute><AiMarketTrendParameterQueryPage /></ProtectedRoute>} />
        <Route path="/ai-market-trend-property/queries" element={<ProtectedRoute><AiMarketTrendPropertyQueryPage /></ProtectedRoute>} />
        <Route path="/user-profile-document/queries" element={<ProtectedRoute><UserProfileDocumentQueryPage /></ProtectedRoute>} />
        <Route path="/institution-profile-document/queries" element={<ProtectedRoute><InstitutionProfileDocumentQueryPage /></ProtectedRoute>} />
        <Route path="/course-document-group/queries" element={<ProtectedRoute><CourseDocumentGroupQueryPage /></ProtectedRoute>} />
        <Route path="/course-document/queries" element={<ProtectedRoute><CourseDocumentQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-document/queries" element={<ProtectedRoute><MarketTrendDocumentQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-document/queries" element={<ProtectedRoute><JobPostDocumentQueryPage /></ProtectedRoute>} />
        <Route path="/user-education/queries" element={<ProtectedRoute><UserEducationQueryPage /></ProtectedRoute>} />
        <Route path="/user-work-experience/queries" element={<ProtectedRoute><UserWorkExperienceQueryPage /></ProtectedRoute>} />
        <Route path="/user-skill/queries" element={<ProtectedRoute><UserSkillQueryPage /></ProtectedRoute>} />
        <Route path="/user-certification/queries" element={<ProtectedRoute><UserCertificationQueryPage /></ProtectedRoute>} />
        <Route path="/user-language/queries" element={<ProtectedRoute><UserLanguageQueryPage /></ProtectedRoute>} />
        <Route path="/user-achievement/queries" element={<ProtectedRoute><UserAchievementQueryPage /></ProtectedRoute>} />
        <Route path="/user-social-link/queries" element={<ProtectedRoute><UserSocialLinkQueryPage /></ProtectedRoute>} />
        <Route path="/institution-department/queries" element={<ProtectedRoute><InstitutionDepartmentQueryPage /></ProtectedRoute>} />
        <Route path="/institution-location/queries" element={<ProtectedRoute><InstitutionLocationQueryPage /></ProtectedRoute>} />
        <Route path="/institution-accreditation/queries" element={<ProtectedRoute><InstitutionAccreditationQueryPage /></ProtectedRoute>} />
        <Route path="/institution-ranking/queries" element={<ProtectedRoute><InstitutionRankingQueryPage /></ProtectedRoute>} />
        <Route path="/institution-facility/queries" element={<ProtectedRoute><InstitutionFacilityQueryPage /></ProtectedRoute>} />
        <Route path="/course-module/queries" element={<ProtectedRoute><CourseModuleQueryPage /></ProtectedRoute>} />
        <Route path="/course-lesson/queries" element={<ProtectedRoute><CourseLessonQueryPage /></ProtectedRoute>} />
        <Route path="/course-prerequisite/queries" element={<ProtectedRoute><CoursePrerequisiteQueryPage /></ProtectedRoute>} />
        <Route path="/course-instructor/queries" element={<ProtectedRoute><CourseInstructorQueryPage /></ProtectedRoute>} />
        <Route path="/course-review/queries" element={<ProtectedRoute><CourseReviewQueryPage /></ProtectedRoute>} />
        <Route path="/course-assignment/queries" element={<ProtectedRoute><CourseAssignmentQueryPage /></ProtectedRoute>} />
        <Route path="/user-course-progress/queries" element={<ProtectedRoute><UserCourseProgressQueryPage /></ProtectedRoute>} />
        <Route path="/user-assignment-submission/queries" element={<ProtectedRoute><UserAssignmentSubmissionQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-requirement/queries" element={<ProtectedRoute><JobPostRequirementQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-benefit/queries" element={<ProtectedRoute><JobPostBenefitQueryPage /></ProtectedRoute>} />
        <Route path="/job-application/queries" element={<ProtectedRoute><JobApplicationQueryPage /></ProtectedRoute>} />
        <Route path="/job-interview/queries" element={<ProtectedRoute><JobInterviewQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-question/queries" element={<ProtectedRoute><JobPostQuestionQueryPage /></ProtectedRoute>} />
        <Route path="/job-application-answer/queries" element={<ProtectedRoute><JobApplicationAnswerQueryPage /></ProtectedRoute>} />
        <Route path="/community-category/queries" element={<ProtectedRoute><CommunityCategoryQueryPage /></ProtectedRoute>} />
        <Route path="/community-rule/queries" element={<ProtectedRoute><CommunityRuleQueryPage /></ProtectedRoute>} />
        <Route path="/community-event/queries" element={<ProtectedRoute><CommunityEventQueryPage /></ProtectedRoute>} />
        <Route path="/community-event-attendee/queries" element={<ProtectedRoute><CommunityEventAttendeeQueryPage /></ProtectedRoute>} />
        <Route path="/post-attachment/queries" element={<ProtectedRoute><PostAttachmentQueryPage /></ProtectedRoute>} />
        <Route path="/post-tag/queries" element={<ProtectedRoute><PostTagQueryPage /></ProtectedRoute>} />
        <Route path="/post-tag-link/queries" element={<ProtectedRoute><PostTagLinkQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-skill-demand/queries" element={<ProtectedRoute><MarketTrendSkillDemandQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-industry/queries" element={<ProtectedRoute><MarketTrendIndustryQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-location/queries" element={<ProtectedRoute><MarketTrendLocationQueryPage /></ProtectedRoute>} />
        <Route path="/user-skill-endorsement/queries" element={<ProtectedRoute><UserSkillEndorsementQueryPage /></ProtectedRoute>} />
        <Route path="/user-recommendation/queries" element={<ProtectedRoute><UserRecommendationQueryPage /></ProtectedRoute>} />
        <Route path="/notification/queries" element={<ProtectedRoute><NotificationQueryPage /></ProtectedRoute>} />
        <Route path="/course-job-post-link/queries" element={<ProtectedRoute><CourseJobPostLinkQueryPage /></ProtectedRoute>} />
        <Route path="/course-community-link/queries" element={<ProtectedRoute><CourseCommunityLinkQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-community-link/queries" element={<ProtectedRoute><JobPostCommunityLinkQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-course-link/queries" element={<ProtectedRoute><MarketTrendCourseLinkQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-job-post-link/queries" element={<ProtectedRoute><MarketTrendJobPostLinkQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-institution-link/queries" element={<ProtectedRoute><MarketTrendInstitutionLinkQueryPage /></ProtectedRoute>} />
        <Route path="/user-file/queries" element={<ProtectedRoute><UserFileQueryPage /></ProtectedRoute>} />
        <Route path="/institution-file/queries" element={<ProtectedRoute><InstitutionFileQueryPage /></ProtectedRoute>} />
        <Route path="/course-file/queries" element={<ProtectedRoute><CourseFileQueryPage /></ProtectedRoute>} />
        <Route path="/job-post-file/queries" element={<ProtectedRoute><JobPostFileQueryPage /></ProtectedRoute>} />
        <Route path="/community-file/queries" element={<ProtectedRoute><CommunityFileQueryPage /></ProtectedRoute>} />
        <Route path="/market-trend-file/queries" element={<ProtectedRoute><MarketTrendFileQueryPage /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/user" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
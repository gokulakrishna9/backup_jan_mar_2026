import { configureStore } from '@reduxjs/toolkit';
import studentProfileReducer from './slices/studentProfileSlice';
import employerProfileReducer from './slices/employerProfileSlice';
import trainerProfileReducer from './slices/trainerProfileSlice';
import jobPostingReducer from './slices/jobPostingSlice';
import trainingProgramReducer from './slices/trainingProgramSlice';
import jobApplicationReducer from './slices/jobApplicationSlice';
import trainingEnrollmentReducer from './slices/trainingEnrollmentSlice';
import userProfileReducer from './slices/userProfileSlice';
import educationLevelReducer from './slices/educationLevelSlice';
import fieldOfStudyReducer from './slices/fieldOfStudySlice';
import institutionReducer from './slices/institutionSlice';
import userEducationReducer from './slices/userEducationSlice';
import industryReducer from './slices/industrySlice';
import jobTitleReducer from './slices/jobTitleSlice';
import userWorkExperienceReducer from './slices/userWorkExperienceSlice';
import skillCategoryReducer from './slices/skillCategorySlice';
import skillReducer from './slices/skillSlice';
import userSkillReducer from './slices/userSkillSlice';
import trainingModuleReducer from './slices/trainingModuleSlice';
import moduleProgressReducer from './slices/moduleProgressSlice';
import trainingExamReducer from './slices/trainingExamSlice';
import examAttemptReducer from './slices/examAttemptSlice';
import trainingCertificationReducer from './slices/trainingCertificationSlice';
import courseDocumentReducer from './slices/courseDocumentSlice';
import courseVideoReducer from './slices/courseVideoSlice';
import courseAudioReducer from './slices/courseAudioSlice';
import courseCodeLabReducer from './slices/courseCodeLabSlice';
import examQuestionReducer from './slices/examQuestionSlice';
import examAnswerReducer from './slices/examAnswerSlice';
import courseQuestionReducer from './slices/courseQuestionSlice';
import courseAnswerReducer from './slices/courseAnswerSlice';
import companyReducer from './slices/companySlice';
import locationReducer from './slices/locationSlice';


export const store = configureStore({
  reducer: {
    studentProfile: studentProfileReducer,
    employerProfile: employerProfileReducer,
    trainerProfile: trainerProfileReducer,
    jobPosting: jobPostingReducer,
    trainingProgram: trainingProgramReducer,
    jobApplication: jobApplicationReducer,
    trainingEnrollment: trainingEnrollmentReducer,
    userProfile: userProfileReducer,
    educationLevel: educationLevelReducer,
    fieldOfStudy: fieldOfStudyReducer,
    institution: institutionReducer,
    userEducation: userEducationReducer,
    industry: industryReducer,
    jobTitle: jobTitleReducer,
    userWorkExperience: userWorkExperienceReducer,
    skillCategory: skillCategoryReducer,
    skill: skillReducer,
    userSkill: userSkillReducer,
    trainingModule: trainingModuleReducer,
    moduleProgress: moduleProgressReducer,
    trainingExam: trainingExamReducer,
    examAttempt: examAttemptReducer,
    trainingCertification: trainingCertificationReducer,
    courseDocument: courseDocumentReducer,
    courseVideo: courseVideoReducer,
    courseAudio: courseAudioReducer,
    courseCodeLab: courseCodeLabReducer,
    examQuestion: examQuestionReducer,
    examAnswer: examAnswerReducer,
    courseQuestion: courseQuestionReducer,
    courseAnswer: courseAnswerReducer,
    company: companyReducer,
    location: locationReducer,
  },
});
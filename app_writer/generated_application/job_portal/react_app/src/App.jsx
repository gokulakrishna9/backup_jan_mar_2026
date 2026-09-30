import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './auth/ProtectedRoute';
import LoginPage from './auth/LoginPage';
import RegisterPage from './auth/RegisterPage';
import AppLayout from './layout/AppLayout';
import DashboardPage from './pages/dashboard/DashboardPage';
import UserProfilePage from './pages/profiles/UserProfilePage';
import UserEducationPage from './pages/resume/UserEducationPage';
import JobPostingPage from './pages/jobs/JobPostingPage';
import JobApplicationPage from './pages/jobs/JobApplicationPage';
import TrainingProgramPage from './pages/training/TrainingProgramPage';
import TrainingExamPage from './pages/training/TrainingExamPage';
import CourseQuestionPage from './pages/training/CourseQuestionPage';
import TrainingEnrollmentPage from './pages/learning/TrainingEnrollmentPage';
import TrainingCertificationPage from './pages/learning/TrainingCertificationPage';
import EducationLevelPage from './pages/masters/EducationLevelPage';
import FieldOfStudyPage from './pages/masters/FieldOfStudyPage';
import InstitutionPage from './pages/masters/InstitutionPage';
import IndustryPage from './pages/masters/IndustryPage';
import JobTitlePage from './pages/masters/JobTitlePage';
import SkillCategoryPage from './pages/masters/SkillCategoryPage';
import SkillPage from './pages/masters/SkillPage';
import CompanyPage from './pages/masters/CompanyPage';
import LocationPage from './pages/masters/LocationPage';


function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route element={<AppLayout />}>
        <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
        <Route path="/my-profile" element={<ProtectedRoute><UserProfilePage /></ProtectedRoute>} />
        <Route path="/my-resume" element={<ProtectedRoute><UserEducationPage /></ProtectedRoute>} />
        <Route path="/jobs" element={<ProtectedRoute><JobPostingPage /></ProtectedRoute>} />
        <Route path="/my-applications" element={<ProtectedRoute><JobApplicationPage /></ProtectedRoute>} />
        <Route path="/training-programs" element={<ProtectedRoute><TrainingProgramPage /></ProtectedRoute>} />
        <Route path="/exams" element={<ProtectedRoute><TrainingExamPage /></ProtectedRoute>} />
        <Route path="/qa" element={<ProtectedRoute><CourseQuestionPage /></ProtectedRoute>} />
        <Route path="/my-enrollments" element={<ProtectedRoute><TrainingEnrollmentPage /></ProtectedRoute>} />
        <Route path="/my-certifications" element={<ProtectedRoute><TrainingCertificationPage /></ProtectedRoute>} />
        <Route path="/masters/education-levels" element={<ProtectedRoute><EducationLevelPage /></ProtectedRoute>} />
        <Route path="/masters/fields-of-study" element={<ProtectedRoute><FieldOfStudyPage /></ProtectedRoute>} />
        <Route path="/masters/institutions" element={<ProtectedRoute><InstitutionPage /></ProtectedRoute>} />
        <Route path="/masters/industries" element={<ProtectedRoute><IndustryPage /></ProtectedRoute>} />
        <Route path="/masters/job-titles" element={<ProtectedRoute><JobTitlePage /></ProtectedRoute>} />
        <Route path="/masters/skill-categories" element={<ProtectedRoute><SkillCategoryPage /></ProtectedRoute>} />
        <Route path="/masters/skills" element={<ProtectedRoute><SkillPage /></ProtectedRoute>} />
        <Route path="/masters/companies" element={<ProtectedRoute><CompanyPage /></ProtectedRoute>} />
        <Route path="/masters/locations" element={<ProtectedRoute><LocationPage /></ProtectedRoute>} />
        <Route path="/" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
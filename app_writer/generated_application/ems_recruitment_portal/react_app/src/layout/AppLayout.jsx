import React, { useState, useEffect, useRef } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { Button } from 'primereact/button';
import './AppLayout.css';

const AppLayout = () => {
  const location = useLocation();
  const navRef = useRef(null);
  const [headerCollapsed, setHeaderCollapsed] = useState(false);
  const [leftNavCollapsed, setLeftNavCollapsed] = useState(false);
  const [footerCollapsed, setFooterCollapsed] = useState(false);


  useEffect(() => {
    const activeEl = navRef.current?.querySelector('.active-link');
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [location.pathname]);

  return (
    <div className={`app-layout${headerCollapsed ? ' header-collapsed' : ''}${leftNavCollapsed ? ' leftnav-collapsed' : ''}${footerCollapsed ? ' footer-collapsed' : ''}`}>
      <div className="header-wrapper">
        <header className="app-header">
          <h1 className="header-title">Ems Recruitment Portal</h1>
        </header>
        <Button icon={headerCollapsed ? 'pi pi-angle-down' : 'pi pi-angle-up'} className="p-button-rounded header-collapse-btn" onClick={() => setHeaderCollapsed(!headerCollapsed)} />
      </div>

      <div className="leftnav-wrapper">
        <nav className="app-leftnav">
          <div className="nav-content" ref={navRef}>
            <div className="nav-group">
              <h4>Ems</h4>
              <ul>
                <li><NavLink to="/ai-community-post-evaluation" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Community Post Evaluation</NavLink></li>
                <li><NavLink to="/ai-evaluation-parameter" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Evaluation Parameter</NavLink></li>
                <li><NavLink to="/ai-evaluation-parameter-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Evaluation Parameter Group</NavLink></li>
                <li><NavLink to="/ai-institution-profile-evaluation" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Institution Profile Evaluation</NavLink></li>
                <li><NavLink to="/ai-job-recommendation" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Job Recommendation</NavLink></li>
                <li><NavLink to="/ai-market-trend-parameter" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Market Trend Parameter</NavLink></li>
                <li><NavLink to="/ai-market-trend-parameter-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Market Trend Parameter Group</NavLink></li>
                <li><NavLink to="/ai-market-trend-property" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai Market Trend Property</NavLink></li>
                <li><NavLink to="/ai-user-profile-evaluation" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai User Profile Evaluation</NavLink></li>
                <li><NavLink to="/ai-user-profile-evaluation-parameter" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai User Profile Evaluation Parameter</NavLink></li>
                <li><NavLink to="/ai-user-profile-evaluation-parameter-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Ai User Profile Evaluation Parameter Group</NavLink></li>
                <li><NavLink to="/candidate-institute-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Candidate Institute Link</NavLink></li>
                <li><NavLink to="/community" className={({ isActive }) => isActive ? 'active-link' : ''}>Community</NavLink></li>
                <li><NavLink to="/community-category" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Category</NavLink></li>
                <li><NavLink to="/community-event" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Event</NavLink></li>
                <li><NavLink to="/community-event-attendee" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Event Attendee</NavLink></li>
                <li><NavLink to="/community-file" className={({ isActive }) => isActive ? 'active-link' : ''}>Community File</NavLink></li>
                <li><NavLink to="/community-post-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Post Link</NavLink></li>
                <li><NavLink to="/community-property" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Property</NavLink></li>
                <li><NavLink to="/community-property-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Property Group</NavLink></li>
                <li><NavLink to="/community-property-user-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Property User Link</NavLink></li>
                <li><NavLink to="/community-rule" className={({ isActive }) => isActive ? 'active-link' : ''}>Community Rule</NavLink></li>
                <li><NavLink to="/community-user-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Community User Link</NavLink></li>
                <li><NavLink to="/community-user-post" className={({ isActive }) => isActive ? 'active-link' : ''}>Community User Post</NavLink></li>
                <li><NavLink to="/course" className={({ isActive }) => isActive ? 'active-link' : ''}>Course</NavLink></li>
                <li><NavLink to="/course-assignment" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Assignment</NavLink></li>
                <li><NavLink to="/course-community-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Community Link</NavLink></li>
                <li><NavLink to="/course-document" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Document</NavLink></li>
                <li><NavLink to="/course-document-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Document Group</NavLink></li>
                <li><NavLink to="/course-file" className={({ isActive }) => isActive ? 'active-link' : ''}>Course File</NavLink></li>
                <li><NavLink to="/course-instructor" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Instructor</NavLink></li>
                <li><NavLink to="/course-job-post-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Job Post Link</NavLink></li>
                <li><NavLink to="/course-lesson" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Lesson</NavLink></li>
                <li><NavLink to="/course-module" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Module</NavLink></li>
                <li><NavLink to="/course-prerequisite" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Prerequisite</NavLink></li>
                <li><NavLink to="/course-property" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Property</NavLink></li>
                <li><NavLink to="/course-property-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Property Group</NavLink></li>
                <li><NavLink to="/course-review" className={({ isActive }) => isActive ? 'active-link' : ''}>Course Review</NavLink></li>
                <li><NavLink to="/emogi-post-user-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Emogi Post User Link</NavLink></li>
                <li><NavLink to="/institution" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution</NavLink></li>
                <li><NavLink to="/institution-accreditation" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Accreditation</NavLink></li>
                <li><NavLink to="/institution-department" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Department</NavLink></li>
                <li><NavLink to="/institution-facility" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Facility</NavLink></li>
                <li><NavLink to="/institution-file" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution File</NavLink></li>
                <li><NavLink to="/institution-location" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Location</NavLink></li>
                <li><NavLink to="/institution-profile-document" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Profile Document</NavLink></li>
                <li><NavLink to="/institution-property" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Property</NavLink></li>
                <li><NavLink to="/institution-property-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Property Group</NavLink></li>
                <li><NavLink to="/institution-ranking" className={({ isActive }) => isActive ? 'active-link' : ''}>Institution Ranking</NavLink></li>
                <li><NavLink to="/job-application" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Application</NavLink></li>
                <li><NavLink to="/job-application-answer" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Application Answer</NavLink></li>
                <li><NavLink to="/job-interview" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Interview</NavLink></li>
                <li><NavLink to="/job-post" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post</NavLink></li>
                <li><NavLink to="/job-post-benefit" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Benefit</NavLink></li>
                <li><NavLink to="/job-post-community-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Community Link</NavLink></li>
                <li><NavLink to="/job-post-document" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Document</NavLink></li>
                <li><NavLink to="/job-post-file" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post File</NavLink></li>
                <li><NavLink to="/job-post-property" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Property</NavLink></li>
                <li><NavLink to="/job-post-property-group" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Property Group</NavLink></li>
                <li><NavLink to="/job-post-question" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Question</NavLink></li>
                <li><NavLink to="/job-post-requirement" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post Requirement</NavLink></li>
                <li><NavLink to="/job-post-user-bookmark" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Post User Bookmark</NavLink></li>
                <li><NavLink to="/market-trend-course-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Course Link</NavLink></li>
                <li><NavLink to="/market-trend-document" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Document</NavLink></li>
                <li><NavLink to="/market-trend-file" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend File</NavLink></li>
                <li><NavLink to="/market-trend-industry" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Industry</NavLink></li>
                <li><NavLink to="/market-trend-institution-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Institution Link</NavLink></li>
                <li><NavLink to="/market-trend-job-post-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Job Post Link</NavLink></li>
                <li><NavLink to="/market-trend-location" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Location</NavLink></li>
                <li><NavLink to="/market-trend-skill-demand" className={({ isActive }) => isActive ? 'active-link' : ''}>Market Trend Skill Demand</NavLink></li>
                <li><NavLink to="/notification" className={({ isActive }) => isActive ? 'active-link' : ''}>Notification</NavLink></li>
                <li><NavLink to="/post-attachment" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Attachment</NavLink></li>
                <li><NavLink to="/post-comment" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Comment</NavLink></li>
                <li><NavLink to="/post-comment-emogi-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Comment Emogi Link</NavLink></li>
                <li><NavLink to="/post-emogi" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Emogi</NavLink></li>
                <li><NavLink to="/post-flag" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Flag</NavLink></li>
                <li><NavLink to="/post-tag" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Tag</NavLink></li>
                <li><NavLink to="/post-tag-link" className={({ isActive }) => isActive ? 'active-link' : ''}>Post Tag Link</NavLink></li>
                <li><NavLink to="/subscription-payment-history" className={({ isActive }) => isActive ? 'active-link' : ''}>Subscription Payment History</NavLink></li>
                <li><NavLink to="/user" className={({ isActive }) => isActive ? 'active-link' : ''}>User</NavLink></li>
                <li><NavLink to="/user-achievement" className={({ isActive }) => isActive ? 'active-link' : ''}>User Achievement</NavLink></li>
                <li><NavLink to="/user-assignment-submission" className={({ isActive }) => isActive ? 'active-link' : ''}>User Assignment Submission</NavLink></li>
                <li><NavLink to="/user-certification" className={({ isActive }) => isActive ? 'active-link' : ''}>User Certification</NavLink></li>
                <li><NavLink to="/user-course-link" className={({ isActive }) => isActive ? 'active-link' : ''}>User Course Link</NavLink></li>
                <li><NavLink to="/user-course-progress" className={({ isActive }) => isActive ? 'active-link' : ''}>User Course Progress</NavLink></li>
                <li><NavLink to="/user-course-purchase" className={({ isActive }) => isActive ? 'active-link' : ''}>User Course Purchase</NavLink></li>
                <li><NavLink to="/user-course-wishlist" className={({ isActive }) => isActive ? 'active-link' : ''}>User Course Wishlist</NavLink></li>
                <li><NavLink to="/user-education" className={({ isActive }) => isActive ? 'active-link' : ''}>User Education</NavLink></li>
                <li><NavLink to="/user-file" className={({ isActive }) => isActive ? 'active-link' : ''}>User File</NavLink></li>
                <li><NavLink to="/user-institute-property-link" className={({ isActive }) => isActive ? 'active-link' : ''}>User Institute Property Link</NavLink></li>
                <li><NavLink to="/user-job-post-bookmark" className={({ isActive }) => isActive ? 'active-link' : ''}>User Job Post Bookmark</NavLink></li>
                <li><NavLink to="/user-language" className={({ isActive }) => isActive ? 'active-link' : ''}>User Language</NavLink></li>
                <li><NavLink to="/user-profile-document" className={({ isActive }) => isActive ? 'active-link' : ''}>User Profile Document</NavLink></li>
                <li><NavLink to="/user-property" className={({ isActive }) => isActive ? 'active-link' : ''}>User Property</NavLink></li>
                <li><NavLink to="/user-property-group" className={({ isActive }) => isActive ? 'active-link' : ''}>User Property Group</NavLink></li>
                <li><NavLink to="/user-recommendation" className={({ isActive }) => isActive ? 'active-link' : ''}>User Recommendation</NavLink></li>
                <li><NavLink to="/user-skill" className={({ isActive }) => isActive ? 'active-link' : ''}>User Skill</NavLink></li>
                <li><NavLink to="/user-skill-endorsement" className={({ isActive }) => isActive ? 'active-link' : ''}>User Skill Endorsement</NavLink></li>
                <li><NavLink to="/user-social-link" className={({ isActive }) => isActive ? 'active-link' : ''}>User Social Link</NavLink></li>
                <li><NavLink to="/user-work-experience" className={({ isActive }) => isActive ? 'active-link' : ''}>User Work Experience</NavLink></li>
              </ul>
            </div>
          </div>
        </nav>
        <Button icon={leftNavCollapsed ? 'pi pi-angle-right' : 'pi pi-angle-left'} className="p-button-rounded nav-collapse-btn" onClick={() => setLeftNavCollapsed(!leftNavCollapsed)} />
      </div>


      <main className="app-content">
        <Outlet />
      </main>

      <div className="footer-wrapper">
        <Button icon={footerCollapsed ? 'pi pi-angle-up' : 'pi pi-angle-down'} className="p-button-rounded footer-collapse-btn" onClick={() => setFooterCollapsed(!footerCollapsed)} />
        <footer className="app-footer">
          <span className="footer-text">&copy; Ems Recruitment Portal</span>
        </footer>
      </div>
    </div>
  );
};

export default AppLayout;
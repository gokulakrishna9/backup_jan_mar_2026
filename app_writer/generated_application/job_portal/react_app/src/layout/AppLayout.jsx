import React, { useState, useEffect, useRef } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { Button } from 'primereact/button';
import './AppLayout.css';

const AppLayout = () => {
  const location = useLocation();
  const navRef = useRef(null);
  const [leftNavCollapsed, setLeftNavCollapsed] = useState(false);


  useEffect(() => {
    const activeEl = navRef.current?.querySelector('.active-link');
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [location.pathname]);

  return (
    <div className={`app-layout${leftNavCollapsed ? ' leftnav-collapsed' : ''}`}>
      <div className="header-wrapper">
        <header className="app-header">
          <h1 className="header-title">Job Portal</h1>
        </header>
      </div>

      <div className="leftnav-wrapper">
        <nav className="app-leftnav">
          <div className="nav-content" ref={navRef}>
            <div className="nav-group">
              <h4>Dashboard</h4>
              <ul>
                <li><NavLink to="/" className={({ isActive }) => isActive ? 'active-link' : ''}>Dashboard</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>My Profile</h4>
              <ul>
                <li><NavLink to="/my-profile" className={({ isActive }) => isActive ? 'active-link' : ''}>My Profile</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>My Resume</h4>
              <ul>
                <li><NavLink to="/my-resume" className={({ isActive }) => isActive ? 'active-link' : ''}>My Resume</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>Jobs</h4>
              <ul>
                <li><NavLink to="/jobs" className={({ isActive }) => isActive ? 'active-link' : ''}>Browse Jobs</NavLink></li>
                <li><NavLink to="/my-applications" className={({ isActive }) => isActive ? 'active-link' : ''}>My Applications</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>Training</h4>
              <ul>
                <li><NavLink to="/training-programs" className={({ isActive }) => isActive ? 'active-link' : ''}>Programs</NavLink></li>
                <li><NavLink to="/exams" className={({ isActive }) => isActive ? 'active-link' : ''}>Exams</NavLink></li>
                <li><NavLink to="/qa" className={({ isActive }) => isActive ? 'active-link' : ''}>Q&A</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>My Learning</h4>
              <ul>
                <li><NavLink to="/my-enrollments" className={({ isActive }) => isActive ? 'active-link' : ''}>Enrollments</NavLink></li>
                <li><NavLink to="/my-certifications" className={({ isActive }) => isActive ? 'active-link' : ''}>Certifications</NavLink></li>
              </ul>
            </div>
            <div className="nav-group">
              <h4>Masters</h4>
              <ul>
                <li><NavLink to="/masters/education-levels" className={({ isActive }) => isActive ? 'active-link' : ''}>Education Levels</NavLink></li>
                <li><NavLink to="/masters/fields-of-study" className={({ isActive }) => isActive ? 'active-link' : ''}>Fields of Study</NavLink></li>
                <li><NavLink to="/masters/institutions" className={({ isActive }) => isActive ? 'active-link' : ''}>Institutions</NavLink></li>
                <li><NavLink to="/masters/industries" className={({ isActive }) => isActive ? 'active-link' : ''}>Industries</NavLink></li>
                <li><NavLink to="/masters/job-titles" className={({ isActive }) => isActive ? 'active-link' : ''}>Job Titles</NavLink></li>
                <li><NavLink to="/masters/skill-categories" className={({ isActive }) => isActive ? 'active-link' : ''}>Skill Categories</NavLink></li>
                <li><NavLink to="/masters/skills" className={({ isActive }) => isActive ? 'active-link' : ''}>Skills</NavLink></li>
                <li><NavLink to="/masters/companies" className={({ isActive }) => isActive ? 'active-link' : ''}>Companies</NavLink></li>
                <li><NavLink to="/masters/locations" className={({ isActive }) => isActive ? 'active-link' : ''}>Locations</NavLink></li>
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
        <footer className="app-footer">
          <span className="footer-text">&copy; Job Portal</span>
        </footer>
      </div>
    </div>
  );
};

export default AppLayout;
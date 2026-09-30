"""Jinja2 templates for AppLayout.jsx and AppLayout.css."""

APP_LAYOUT_JSX = """import React, { useState, useEffect, useRef } from 'react';
import { Outlet, NavLink, useLocation } from 'react-router-dom';
import { Button } from 'primereact/button';
import './AppLayout.css';

const AppLayout = () => {
  const location = useLocation();
  const navRef = useRef(null);
{% if header.collapsible %}  const [headerCollapsed, setHeaderCollapsed] = useState({{ 'true' if header.defaultCollapsed else 'false' }});
{% endif %}{% if leftNav.collapsible %}  const [leftNavCollapsed, setLeftNavCollapsed] = useState({{ 'true' if leftNav.defaultCollapsed else 'false' }});
{% endif %}{% if footer.collapsible %}  const [footerCollapsed, setFooterCollapsed] = useState({{ 'true' if footer.defaultCollapsed else 'false' }});
{% endif %}

  useEffect(() => {
    const activeEl = navRef.current?.querySelector('.active-link');
    if (activeEl) {
      activeEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
  }, [location.pathname]);

  return (
    <div className={`app-layout{% if header.collapsible %}${headerCollapsed ? ' header-collapsed' : ''}{% endif %}{% if leftNav.collapsible %}${leftNavCollapsed ? ' leftnav-collapsed' : ''}{% endif %}{% if footer.collapsible %}${footerCollapsed ? ' footer-collapsed' : ''}{% endif %}`}>
{% if header.visible %}      <div className="header-wrapper">
        <header className="app-header">
          <h1 className="header-title">{{ applicationName }}</h1>
        </header>
{% if header.collapsible %}        <Button icon={headerCollapsed ? 'pi pi-angle-down' : 'pi pi-angle-up'} className="p-button-rounded header-collapse-btn" onClick={() => setHeaderCollapsed(!headerCollapsed)} />
{% endif %}      </div>
{% endif %}
{% if leftNav.visible %}      <div className="leftnav-wrapper">
        <nav className="app-leftnav">
          <div className="nav-content" ref={navRef}>
{% for group in navGroups %}            <div className="nav-group">
              <h4>{{ group.groupName }}</h4>
              <ul>
{% for entity in group.entities %}                <li><NavLink to="{{ entity.path }}" className={({ isActive }) => isActive ? 'active-link' : ''}>{{ entity.label }}</NavLink></li>
{% endfor %}              </ul>
            </div>
{% endfor %}          </div>
        </nav>
{% if leftNav.collapsible %}        <Button icon={leftNavCollapsed ? 'pi pi-angle-right' : 'pi pi-angle-left'} className="p-button-rounded nav-collapse-btn" onClick={() => setLeftNavCollapsed(!leftNavCollapsed)} />
{% endif %}      </div>
{% endif %}

      <main className="app-content">
        <Outlet />
      </main>

{% if footer.visible %}      <div className="footer-wrapper">
{% if footer.collapsible %}        <Button icon={footerCollapsed ? 'pi pi-angle-up' : 'pi pi-angle-down'} className="p-button-rounded footer-collapse-btn" onClick={() => setFooterCollapsed(!footerCollapsed)} />
{% endif %}        <footer className="app-footer">
          <span className="footer-text">&copy; {{ applicationName }}</span>
        </footer>
      </div>
{% endif %}    </div>
  );
};

export default AppLayout;
"""

APP_LAYOUT_CSS = """.app-layout {
  display: grid;
  grid-template-rows: auto 1fr auto;
  grid-template-columns: {% if leftNav.visible %}250px{% else %}0{% endif %} 1fr;
  grid-template-areas:
    "header header"
    "leftnav content"
    "footer footer";
  min-height: 100vh;
  transition: grid-template-columns 300ms ease-out;
}

/* ── Header ── */
.header-wrapper {
  grid-area: header;
  position: sticky;
  top: 0;
  z-index: 50;
}

.app-header {
  background: var(--primary-color, #6366f1);
  color: white;
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  transition: padding 300ms ease-out, max-height 300ms ease-out;
  max-height: 80px;
  overflow: hidden;
}

.header-title {
  margin: 0;
  font-size: 1.25rem;
  white-space: nowrap;
  overflow: hidden;
  transition: opacity 300ms ease-out;
  opacity: 1;
}

.header-collapse-btn {
  position: absolute;
  bottom: -14px;
  right: 1.5rem;
  z-index: 100;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  padding: 0 !important;
  background: var(--primary-color, #6366f1) !important;
  color: white !important;
  border: 2px solid white !important;
  border-radius: 50% !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.header-collapse-btn:hover {
  background: var(--primary-700, #4f46e5) !important;
}

.header-collapse-btn .p-button-icon {
  font-size: 0.7rem;
}

.header-collapsed .app-header {
  max-height: 0;
  padding: 0 1.5rem;
}

.header-collapsed .header-title {
  opacity: 0;
}

/* ── Left Nav ── */
.leftnav-wrapper {
  grid-area: leftnav;
  position: relative;
  width: 250px;
  transition: width 300ms ease-out;
  overflow: visible;
}

.app-leftnav {
  background: var(--surface-ground, #f8f9fa);
  border-right: 1px solid var(--surface-border, #dee2e6);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  position: sticky;
  top: 0;
  max-height: 100vh;
}

.nav-collapse-btn {
  position: absolute;
  top: 50%;
  right: -14px;
  transform: translateY(-50%);
  z-index: 100;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  padding: 0 !important;
  background: var(--primary-color, #6366f1) !important;
  color: white !important;
  border: 2px solid white !important;
  border-radius: 50% !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.nav-collapse-btn:hover {
  background: var(--primary-700, #4f46e5) !important;
}

.nav-collapse-btn .p-button-icon {
  font-size: 0.7rem;
}

.nav-content {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 1rem;
  scrollbar-width: thin;
}

.nav-content::-webkit-scrollbar {
  width: 6px;
}

.nav-content::-webkit-scrollbar-thumb {
  background: var(--surface-border, #dee2e6);
  border-radius: 3px;
}

.nav-content::-webkit-scrollbar-thumb:hover {
  background: var(--text-color-secondary, #6c757d);
}

.nav-group h4 {
  margin: 1rem 0 0.5rem;
  font-size: 0.85rem;
  text-transform: uppercase;
  color: var(--text-color-secondary, #6c757d);
  white-space: nowrap;
}

.nav-group ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-group ul li {
  margin-bottom: 0.25rem;
}

.nav-group ul li a {
  display: block;
  padding: 0.5rem 0.75rem;
  border-radius: 6px;
  color: var(--text-color, #495057);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: background 200ms ease-out;
}

.nav-group ul li a:hover {
  background: var(--surface-hover, #e9ecef);
}

.nav-group ul li a.active-link {
  background: var(--primary-color, #6366f1);
  color: white;
  font-weight: 600;
}

.nav-group ul li a.active-link:hover {
  background: var(--primary-color, #6366f1);
  opacity: 0.9;
}

/* Collapsed leftnav */
.leftnav-collapsed .leftnav-wrapper {
  width: 48px;
}

.leftnav-collapsed .nav-content {
  visibility: hidden;
  opacity: 0;
}

.leftnav-collapsed.app-layout {
  grid-template-columns: 48px 1fr;
}

/* ── Content ── */
.app-content {
  grid-area: content;
  padding: 1.5rem;
  overflow-y: auto;
}

/* ── Footer ── */
.footer-wrapper {
  grid-area: footer;
  position: relative;
}

.app-footer {
  background: var(--surface-ground, #f8f9fa);
  border-top: 1px solid var(--surface-border, #dee2e6);
  padding: 0.5rem 1.5rem;
  display: flex;
  align-items: center;
  transition: padding 300ms ease-out, max-height 300ms ease-out;
  max-height: 60px;
  overflow: hidden;
}

.footer-text {
  white-space: nowrap;
  overflow: hidden;
  transition: opacity 300ms ease-out;
  opacity: 1;
}

.footer-collapse-btn {
  position: absolute;
  top: -14px;
  right: 1.5rem;
  z-index: 100;
  width: 28px !important;
  height: 28px !important;
  min-width: 28px !important;
  padding: 0 !important;
  background: var(--primary-color, #6366f1) !important;
  color: white !important;
  border: 2px solid white !important;
  border-radius: 50% !important;
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}

.footer-collapse-btn:hover {
  background: var(--primary-700, #4f46e5) !important;
}

.footer-collapse-btn .p-button-icon {
  font-size: 0.7rem;
}

.footer-collapsed .app-footer {
  max-height: 0;
  padding: 0 1.5rem;
}

.footer-collapsed .footer-text {
  opacity: 0;
}
"""

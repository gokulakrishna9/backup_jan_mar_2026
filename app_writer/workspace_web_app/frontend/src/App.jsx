import { Routes, Route, Link, useLocation } from 'react-router-dom';
import { useState } from 'react';
import Dashboard from './pages/Dashboard';
import AppDetail from './pages/AppDetail';
import Database from './pages/Database';
import Discussions from './pages/Discussions';
import ChatPanel from './components/ChatPanel';
import GitHubBrowser from './pages/GitHubBrowser';
import AISettings from './pages/AISettings';

/* ── Navigation ── */

const NAV_LINKS = [
  { to: '/', label: 'Dashboard' },
  { to: '/database', label: 'Database' },
  { to: '/discussions', label: 'Discussions' },
  { to: '/github', label: 'GitHub' },
  { to: '/settings/ai', label: 'AI Settings' },
];

function NavBar() {
  const location = useLocation();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-14">
        <Link to="/" className="text-lg font-semibold tracking-tight">Workspace</Link>

        {/* Desktop links */}
        <div className="hidden md:flex space-x-1">
          {NAV_LINKS.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              className={`px-3 py-2 rounded text-sm transition-colors ${
                location.pathname === to
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-300 hover:bg-gray-800 hover:text-white'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Mobile hamburger */}
        <button
          className="md:hidden p-2 rounded hover:bg-gray-800"
          onClick={() => setMobileOpen(!mobileOpen)}
          aria-label="Toggle navigation"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            {mobileOpen
              ? <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              : <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />}
          </svg>
        </button>
      </div>

      {/* Mobile menu */}
      {mobileOpen && (
        <div className="md:hidden px-4 pb-3 space-y-1">
          {NAV_LINKS.map(({ to, label }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setMobileOpen(false)}
              className={`block px-3 py-2 rounded text-sm ${
                location.pathname === to
                  ? 'bg-gray-700 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  );
}

/* ── App ── */

export default function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <NavBar />
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/apps/:name" element={<AppDetail />} />
          <Route path="/database" element={<Database />} />
          <Route path="/discussions" element={<Discussions />} />
          <Route path="/github" element={<GitHubBrowser />} />
          <Route path="/settings/ai" element={<AISettings />} />
        </Routes>
      </main>
      <ChatPanel />
    </div>
  );
}

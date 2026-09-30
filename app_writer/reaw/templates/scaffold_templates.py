"""Jinja2 templates for project scaffold files."""

PACKAGE_JSON = """{
  "name": "{{ applicationName | lower | replace(' ', '-') }}",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.0",
    "@reduxjs/toolkit": "^2.0.0",
    "react-redux": "^9.0.0",
    "axios": "^1.6.0",
    "primereact": "^10.3.0",
    "primeicons": "^6.0.1",
    "primeflex": "^3.3.1",
    "echarts": "^5.4.3",
    "echarts-for-react": "^3.0.2",
    "react-hook-form": "^7.54.0"{% if widgetDependencies %},
{% for dep, ver in widgetDependencies.items() %}    "{{ dep }}": "{{ ver }}"{% if not loop.last %},
{% endif %}{% endfor %}{% endif %}
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "vite": "^5.0.0"
  }
}
"""

VITE_CONFIG = """import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:{{ apiPort }}',
        changeOrigin: true,
      },
    },
  },
});
"""

INDEX_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{{ applicationName }}</title>
  <link rel="stylesheet" href="https://unpkg.com/primereact/resources/themes/lara-light-indigo/theme.css" />
  <link rel="stylesheet" href="https://unpkg.com/primereact/resources/primereact.min.css" />
  <link rel="stylesheet" href="https://unpkg.com/primeicons/primeicons.css" />
  <link rel="stylesheet" href="https://unpkg.com/primeflex/primeflex.css" />
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/src/main.jsx"></script>
</body>
</html>
"""

MAIN_JSX = """import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { Provider } from 'react-redux';
import { store } from './store';
{% if hasAuth %}import { AuthProvider } from './auth/AuthContext';{% endif %}
import App from './App';
import './styles/theme-variables.css';
import './styles/primereact-theme-overrides.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <Provider store={store}>
      <BrowserRouter>
{% if hasAuth %}        <AuthProvider>
          <App />
        </AuthProvider>
{% else %}        <App />
{% endif %}      </BrowserRouter>
    </Provider>
  </React.StrictMode>
);
"""

ENV_FILE = """{% for var in variables %}{% if var.comment %}# {{ var.comment }}
{% endif %}{{ var.key }}={{ var.value }}
{% endfor %}"""

APP_JSX = """import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
{% if hasAuth %}import ProtectedRoute from './auth/ProtectedRoute';
import LoginPage from './auth/LoginPage';
import RegisterPage from './auth/RegisterPage';
{% endif %}import AppLayout from './layout/AppLayout';
{% for route in routes %}import {{ route.pageComponent }} from './pages/{{ route.pageFolder }}/{{ route.pageComponent }}';
{% endfor %}

function App() {
  return (
    <Routes>
{% if hasAuth %}      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
{% endif %}      <Route element={<AppLayout />}>
{% for route in routes %}{% if hasAuth and route.requiresAuth %}        <Route path="{{ route.path }}" element={<ProtectedRoute><{{ route.pageComponent }} /></ProtectedRoute>} />
{% else %}        <Route path="{{ route.path }}" element={<{{ route.pageComponent }} />} />
{% endif %}{% endfor %}        <Route path="/" element={<Navigate to="{{ routes[0].path if routes else '/login' }}" replace />} />
      </Route>
    </Routes>
  );
}

export default App;
"""


LOGGER_UTIL = """/**
 * Client-side logger utility.
 * Controlled by VITE_ENABLE_LOGGING env variable.
 * Logs API errors, network errors, data validation errors, and unhandled exceptions.
 */
const LOGGING_ENABLED = import.meta.env.VITE_ENABLE_LOGGING === 'true';

const formatTimestamp = () => new Date().toISOString();

const logger = {
  /** Log API/HTTP errors (non-2xx responses) */
  apiError: (method, url, status, data) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[API ERROR] ${formatTimestamp()} ${method} ${url} → ${status}`,
      data || ''
    );
  },

  /** Log network errors (no response received) */
  networkError: (method, url, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[NETWORK ERROR] ${formatTimestamp()} ${method} ${url}`,
      error?.message || error
    );
  },

  /** Log data/validation errors (bad payloads, missing fields, parse failures) */
  dataError: (context, message, detail) => {
    if (!LOGGING_ENABLED) return;
    console.warn(
      `[DATA ERROR] ${formatTimestamp()} [${context}]`,
      message,
      detail || ''
    );
  },

  /** Log Redux action errors */
  storeError: (action, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[STORE ERROR] ${formatTimestamp()} ${action}`,
      error?.message || error
    );
  },

  /** Log auth errors (token expired, permission denied) */
  authError: (message, detail) => {
    if (!LOGGING_ENABLED) return;
    console.warn(
      `[AUTH ERROR] ${formatTimestamp()}`,
      message,
      detail || ''
    );
  },

  /** Log render/component errors */
  renderError: (component, error) => {
    if (!LOGGING_ENABLED) return;
    console.error(
      `[RENDER ERROR] ${formatTimestamp()} <${component}>`,
      error?.message || error,
      error?.stack || ''
    );
  },

  /** General info log (only in dev) */
  info: (context, message) => {
    if (!LOGGING_ENABLED) return;
    console.info(`[INFO] ${formatTimestamp()} [${context}]`, message);
  },
};

export default logger;
"""


DASHBOARD_PAGE = """import React from 'react';

const DashboardPage = () => {
  return (
    <div className="grid">
      <div className="col-12">
        <div className="card">
          <h2>Dashboard</h2>
          <p>Welcome to {{ applicationName }}.</p>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
"""

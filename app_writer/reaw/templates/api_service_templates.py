"""Jinja2 templates for API service files."""

API_CLIENT = """import axios from 'axios';
import logger from '../utils/logger';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  headers: {
    'Content-Type': 'application/json',
  },
});

// JWT Bearer token interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — logging + 401 refresh
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const method = error.config?.method?.toUpperCase() || '?';
    const url = error.config?.url || '?';

    if (error.response) {
      // Server responded with non-2xx
      const status = error.response.status;
      if (status === 401) {
        logger.authError('Unauthorized', `${method} ${url}`);
      } else if (status === 403) {
        logger.authError('Forbidden', `${method} ${url}`);
      } else if (status === 422 || status === 400) {
        logger.dataError('API', `Validation error on ${method} ${url}`, error.response.data);
      } else {
        logger.apiError(method, url, status, error.response.data);
      }
    } else if (error.request) {
      // No response received — network error
      logger.networkError(method, url, error);
    } else {
      // Request setup error
      logger.dataError('Request', 'Failed to build request', error.message);
    }

    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
{% if refreshTokenEnabled %}      const refreshToken = localStorage.getItem('refreshToken');
      if (refreshToken) {
        try {
          const baseUrl = import.meta.env.VITE_API_URL || '';
          const { data } = await axios.post(`${baseUrl}/api/auth/refresh`, {
            refreshToken,
          });
          localStorage.setItem('token', data.token);
          if (data.refreshToken) {
            localStorage.setItem('refreshToken', data.refreshToken);
          }
          originalRequest.headers.Authorization = `Bearer ${data.token}`;
          return apiClient(originalRequest);
        } catch (refreshError) {
          logger.authError('Token refresh failed', refreshError.message);
          localStorage.removeItem('token');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }
{% endif %}      localStorage.removeItem('token');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export default apiClient;
"""

ENTITY_SERVICE = """import apiClient from './apiClient';

const BASE_PATH = '{{ basePath }}';

{% if endpoints['create'] is defined and endpoints['create'].enabled %}
export const create{{ entityNamePascal }} = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};
{% endif %}

{% if endpoints['getById'] is defined and endpoints['getById'].enabled %}
export const get{{ entityNamePascal }}ById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};
{% endif %}

{% if endpoints['getAll'] is defined and endpoints['getAll'].enabled %}
export const getAll{{ entityNamePascal }} = async (params = {}) => {
{% if endpoints['getAll'].supportsPagination %}  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
{% else %}  const response = await apiClient.get(BASE_PATH, { params });
{% endif %}  return response.data;
};
{% endif %}

{% if endpoints['update'] is defined and endpoints['update'].enabled %}
export const update{{ entityNamePascal }} = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};
{% endif %}

{% if endpoints['delete'] is defined and endpoints['delete'].enabled %}
export const delete{{ entityNamePascal }} = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};
{% endif %}
"""

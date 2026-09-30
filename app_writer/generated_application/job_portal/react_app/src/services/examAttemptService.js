import apiClient from './apiClient';

const BASE_PATH = '/api/exam_attempts';


export const createExamAttempt = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getExamAttemptById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllExamAttempt = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateExamAttempt = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteExamAttempt = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

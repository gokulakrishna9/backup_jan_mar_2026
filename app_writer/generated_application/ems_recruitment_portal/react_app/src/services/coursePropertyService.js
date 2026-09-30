import apiClient from './apiClient';

const BASE_PATH = '/api/coursepropertys';


export const createCourseProperty = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getCoursePropertyById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllCourseProperty = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateCourseProperty = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteCourseProperty = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

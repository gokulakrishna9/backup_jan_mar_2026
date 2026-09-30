import apiClient from './apiClient';

const BASE_PATH = '/api/institutiondepartments';


export const createInstitutionDepartment = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getInstitutionDepartmentById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllInstitutionDepartment = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateInstitutionDepartment = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteInstitutionDepartment = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

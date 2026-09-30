import apiClient from './apiClient';

const BASE_PATH = '/api/institutionaccreditations';


export const createInstitutionAccreditation = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getInstitutionAccreditationById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllInstitutionAccreditation = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateInstitutionAccreditation = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteInstitutionAccreditation = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

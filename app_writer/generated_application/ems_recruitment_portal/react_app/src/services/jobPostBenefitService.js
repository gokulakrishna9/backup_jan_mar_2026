import apiClient from './apiClient';

const BASE_PATH = '/api/jobpostbenefits';


export const createJobPostBenefit = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getJobPostBenefitById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllJobPostBenefit = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateJobPostBenefit = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteJobPostBenefit = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

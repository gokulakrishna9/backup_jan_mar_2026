import apiClient from './apiClient';

const BASE_PATH = '/api/communityevents';


export const createCommunityEvent = async (data) => {
  const response = await apiClient.post(BASE_PATH, data);
  return response.data;
};



export const getCommunityEventById = async (id) => {
  const response = await apiClient.get(`${BASE_PATH}/${id}`);
  return response.data;
};



export const getAllCommunityEvent = async (params = {}) => {
  const { page = 0, size = 20, sort, filter, ...rest } = params;
  const response = await apiClient.get(BASE_PATH, {
    params: { page, size, sort, filter, ...rest },
  });
  return response.data;
};



export const updateCommunityEvent = async (id, data) => {
  const response = await apiClient.put(`${BASE_PATH}/${id}`, data);
  return response.data;
};



export const deleteCommunityEvent = async (id) => {
  const response = await apiClient.delete(`${BASE_PATH}/${id}`);
  return response.data;
};

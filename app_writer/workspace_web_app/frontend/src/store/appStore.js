import { create } from 'zustand';

const useAppStore = create((set) => ({
  // Selected application
  selectedApp: null,
  setSelectedApp: (app) => set({ selectedApp: app }),

  // Apps list
  apps: [],
  setApps: (apps) => set({ apps }),

  // Loading states
  appsLoading: false,
  setAppsLoading: (loading) => set({ appsLoading: loading }),

  generationLoading: false,
  setGenerationLoading: (loading) => set({ generationLoading: loading }),

  chatLoading: false,
  setChatLoading: (loading) => set({ chatLoading: loading }),
}));

export default useAppStore;

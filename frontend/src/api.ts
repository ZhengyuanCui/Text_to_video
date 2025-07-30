import axios from 'axios';

const api = axios.create({
  baseURL: '/api', // proxy to FastAPI
});

export default api;

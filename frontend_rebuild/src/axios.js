import axiosAPI from 'axios';

const axios = axiosAPI.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { "Content-type": "application/json" }
});

export default axios;

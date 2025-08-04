import axiosAPI from 'axios';

const axios = axiosAPI.create({
  baseURL: import.meta.env.VITE_BASE_URL + '/api',

  headers: { "Content-type": "application/json" }
});

export default axios;

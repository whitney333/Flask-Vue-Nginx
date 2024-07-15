import axiosAPI from 'axios';

const axios = axiosAPI.create({
  baseURL: process.env.VUE_APP_API_URL,
});

export default axios;

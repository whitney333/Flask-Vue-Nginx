import axiosAPI from 'axios';

const axios = axiosAPI.create({
  // local run needs, docker run no
  baseURL: import.meta.env.VITE_BASE_URL,
  headers: { "Content-type": "application/json" }
});

export default axios;

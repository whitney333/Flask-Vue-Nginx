import axiosAPI from 'axios';

const axios = axiosAPI.create({
  headers: { "Content-type": "application/json" }
});

export default axios;

import axios from "axios";

const ENDPOINT = "";

const api = axios.create({
    baseURL: ENDPOINT,
    withCredentials: true
});


export default api;
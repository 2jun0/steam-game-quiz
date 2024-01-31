import axios, { AxiosInstance, CreateAxiosDefaults } from "axios";

const BACKEND_HOST = process.env.NEXT_PUBLIC_BACKEND_HOST;

export function apiAxios(configs?: CreateAxiosDefaults): AxiosInstance {
    const init_configs = {
        baseURL: `${BACKEND_HOST}`
    }

    return axios.create(Object.assign(init_configs, configs))
}
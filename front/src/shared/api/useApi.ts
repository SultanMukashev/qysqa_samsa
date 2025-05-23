'use client'

import axios, { AxiosError } from "axios"

const api = axios.create({
  baseURL: process.env.API_URL  || "http://192.168.20.144:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
})

api.interceptors.request.use((config) => {
  const me = localStorage.getItem("me")
  if (me && JSON.parse(me).user_id) config.headers['Auth'] = `${JSON.parse(me).user_id}`
  return config
})

api.interceptors.response.use(
  (response) => { 
    if (response.headers['auth']) {
      localStorage.setItem("id", response.headers['auth'])
    }
    return response
  },
  (error: AxiosError) => {
    if (error.response?.status === 401) {
      window.location.href = '/auth'
    }
    return Promise.reject(error)
  }
)

export default api
'use client'

import { create } from 'zustand'
import { ApiResponseMessage } from '@/shared/types'
import { LoginRequest, LoginResponse } from '@/features/auth/api/login/type'
import { login } from '@/features/auth/api/login'

export type State = {
  me: LoginResponse | null
}

export type Action = {
  fetchMe: (request: LoginRequest) => Promise<ApiResponseMessage<LoginResponse>>,
  setMe: (me: LoginResponse) => void,
  isAuth: () => boolean
}

export const useMe = create<State & Action>((set) => ({
  me: null,
  fetchMe: async (request): Promise<ApiResponseMessage<LoginResponse>> => {
    const response = await login(request)
    localStorage.setItem('me', JSON.stringify(response.data))
    if (response.ok) {
      set({ me: response.data })
    }
    return response
  },    
  
  setMe: (me) => set({ me }),

  isAuth: () => {
    const me = localStorage.getItem('me')
    return !!me
  },
}))
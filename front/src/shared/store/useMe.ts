'use client'

import { create } from 'zustand'
import { ApiResponseMessage } from '@/shared/types'
import { LoginRequest, LoginResponse } from '@/features/auth/api/login/type'
import { login } from '@/features/auth/api/login'

export type State = {
  me: LoginResponse['data'] | null
}

export type Action = {
  fetchMe: (request: LoginRequest) => Promise<ApiResponseMessage<LoginResponse['data']>>,
  setMe: (me: LoginResponse['data']) => void,
  isAuth: () => boolean
}

export const useMe = create<State & Action>((set) => ({
  me: null,
  fetchMe: async (request): Promise<ApiResponseMessage<LoginResponse['data']>> => {
      const response = await login(request)
      localStorage.setItem('me', JSON.stringify(response.data))
      if (response.ok) {
        set({ me: response.data })
      }
      return response
  },    
  
  setMe: (me) => set({ me }),

  isAuth: () => {
    const token = localStorage.getItem('token')
    const me = localStorage.getItem('me')
    if(me){
      set({me: JSON.parse(me)})
    }
    return !!token
  },
}))
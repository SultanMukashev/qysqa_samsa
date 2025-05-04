'use client'

import { create } from 'zustand'
import { ApiResponseMessage } from '@/shared/types'
import { LoginRequest, LoginResponse } from '@/features/auth/api/login/type'
import { login } from '@/features/auth/api/login'
import { amITeacher } from '@/features/auth/api/amITeacher'
import { LoginTeacherRequest, LoginTeacherResponse } from '@/features/auth/api/loginTeacher/type'
import { loginTeacher } from '@/features/auth/api/loginTeacher'

export type State = {
  me: LoginResponse | null
  teacher: boolean | null
}

export type Action = {
  fetchMeStudent: (request: LoginRequest) => Promise<ApiResponseMessage<LoginResponse>>,
  fetchMeTeacher: (request: LoginTeacherRequest) => Promise<ApiResponseMessage<LoginTeacherResponse>>,
  setMe: (me: LoginResponse) => void,
  setTeacher: (bool: boolean) => void,
  isAuth: () => boolean
}

export const useMe = create<State & Action>((set, get) => ({
  me: null,
  teacher: null,

  fetchMeStudent: async (request) => {
    const response = await login(request)
    localStorage.setItem('me', JSON.stringify(response.data))

    if (response.ok) {
      set({ me: response.data })
      const teacher = await amITeacher()
      localStorage.setItem('teacher', teacher.toString())
      set({ teacher })
    }

    return response
  },

  fetchMeTeacher: async (request) => {
    const response = await loginTeacher(request)
    localStorage.setItem('me', JSON.stringify(response.data))

    if (response.ok) {
      set({ me: response.data })
      const teacher = await amITeacher()
      localStorage.setItem('teacher', teacher.toString())
      set({ teacher })
    }

    return response
  },

  setMe: (me) => set({ me }),

  setTeacher: (bool) => set({ teacher: bool }),

  isAuth: () => {
    const meString = localStorage.getItem('me')
    const teacherString = localStorage.getItem('teacher')

    if (teacherString !== null) {
      console.log(teacherString)
      get().setTeacher(teacherString === 'true')
    }

    if (meString) {
      try {
        const parsed = JSON.parse(meString)
        get().setMe(parsed)
      } catch {
        console.error('Invalid `me` data in localStorage.')
      }
    }

    return !!get().me
  },
}))

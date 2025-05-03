import { create } from 'zustand'
import { GetCoursesResponse } from '../api/getCourses/type'
import { ApiResponseMessage } from '@/shared/types'
import getCourses from '../api/getCourses'

type State = {
  courses: GetCoursesResponse['data'] | null
}

type Action = {
  fetchCourses: () => Promise<ApiResponseMessage<GetCoursesResponse['data']>>
  setCourses: (courses: GetCoursesResponse['data']) => void
}

export const useCourses = create<State & Action>((set) => ({
  courses: null,
  fetchCourses: async() => {
    const response = await getCourses()
    return response
  },
  setCourses: (courses) => set({courses: courses})
}))
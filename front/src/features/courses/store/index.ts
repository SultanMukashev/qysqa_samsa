import { create } from 'zustand'
import { GetCoursesResponse } from '../api/getCourses/type'
import getCourses from '../api/getCourses'

type State = {
  courses: GetCoursesResponse | null
}

type Action = {
  fetchCourses: () => Promise<void>
  setCourses: (courses: GetCoursesResponse) => void
}

export const useCourses = create<State & Action>((set) => ({
  courses: null,
  fetchCourses: async() => {
    const response = await getCourses()

    if(response.ok) {
      set({courses: response.data})
    }
  },
  setCourses: (courses) => set({courses: courses})
}))
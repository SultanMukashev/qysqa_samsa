import { create } from 'zustand'
import { GetSingleCourseResponse } from '../api/type'
import getSingleCourse from '../api'

type State = {
  course: GetSingleCourseResponse | null
}

type Action = {
  fetchCourse: (id: number) => Promise<void>
  setCourse: (course: GetSingleCourseResponse) => void
}

export const useCourse = create<State & Action>((set) => ({
  course: null,
  fetchCourse: async(id: number) => {
    const response = await getSingleCourse(id)

    if(response.ok){
      set({course: response.data})
    }
  },
  setCourse: (course: GetSingleCourseResponse) => set({course: course})
}))
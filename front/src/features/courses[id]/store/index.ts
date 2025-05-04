import { create } from 'zustand'
import { GetSingleCourseResponse } from '../api/getCourse/type'
import getSingleCourse from '../api/getCourse'
import { PostLessonRequest, PostLessonResponse } from '../api/createLesson/type'
import { ApiResponseMessage } from '@/shared/types'
import createLesson from '../api/createLesson'
import getMyCourse from '../api/getCourseTeacher'
import { GetMyCourse } from '../api/getCourseTeacher/type'

type State = {
  course: GetSingleCourseResponse | null | GetMyCourse,
  id: number | null
}

type Action = {
  fetchCourse: (id: number) => Promise<void>
  fetchMyCourseTeacher: (id: number) => Promise<void>
  setCourse: (course: GetSingleCourseResponse) => void
  createLesson: (request: PostLessonRequest) => Promise<ApiResponseMessage<PostLessonResponse>>
}

export const useCourse = create<State & Action>((set) => ({
  course: null,
  id: null,
  fetchCourse: async(id: number) => {
    const response = await getSingleCourse(id)

    if(response.ok){
      set({course: response.data})
    }
  },
  fetchMyCourseTeacher: async(id: number) => {
    const response = await getMyCourse(id)

    if(response.ok){
      set({course: response.data})
    }
  },
  setCourse: (course: GetSingleCourseResponse) => set({course: course}),
  createLesson: async(request: PostLessonRequest) => {
    const response = await createLesson(request)
    return response
  }
}))
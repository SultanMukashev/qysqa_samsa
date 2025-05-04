import { create } from 'zustand'
import { GetTopicResponse } from '../api/getLesson/type'
import getTopic from '../api/getLesson/api'
import { PostLessonRequest, PostLessonResponse } from '../api/uploadFile/type'
import { ApiResponseMessage } from '@/shared/types'
import uploadLesson from '../api/uploadFile/api'

type State = {
  lesson: GetTopicResponse | null
}

type Action = {
  fetchLesson: (id: number) => Promise<void>,
  setLesson: (topic: GetTopicResponse) => void,
  uploadLesson: (id: number, request: PostLessonRequest) => Promise<ApiResponseMessage<PostLessonResponse>>
}

export const useTopic = create<State & Action>((set) => ({
  lesson: null,
  fetchLesson: async(id: number) => {
    const response = await getTopic(id)

    if(response.ok) {
      set({lesson: response.data})
    }
  },
  setLesson: (lesson: GetTopicResponse) => set({lesson: lesson}),
  uploadLesson: async(id: number, request: PostLessonRequest) => {
    const response = await uploadLesson(id, request)

    if(response.ok){
      set({lesson: response.data})
    }

    return response
  }
}))
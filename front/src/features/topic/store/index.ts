import { create } from 'zustand'
import { GetTopicResponse } from '../api/getLesson/type'
import getTopic from '../api/getLesson/api'

type State = {
  topic: GetTopicResponse['data'] | null
}

type Action = {
  fetchTopic: (id: number) => Promise<void>,
  setTopic: (topic: GetTopicResponse['data']) => void
}

export const useTopic = create<State & Action>((set) => ({
  topic: null,
  fetchTopic: async(id: number) => {
    const response = await getTopic(id)

    if(response.ok) {
      set({topic: response.data})
    }
  },
  setTopic: (topic: GetTopicResponse['data']) => set({topic: topic})
}))
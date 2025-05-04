import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { PostLessonRequest, PostLessonResponse } from "./type";

export default async function getCourses (request: PostLessonRequest): Promise<ApiResponseMessage<PostLessonResponse>> {
  try{
    const response = await api.post<PostLessonResponse>('/teachers/lessons', request)

    return {
      ok: true,
      data: response.data,
      message: 'Courses returned successfully'
    }
  }catch(error){
    if (error instanceof AxiosError && error.response?.data){
      return {
        ok: false,
        message: error.response.data.message
      }
    }
  }throw new Error('Network Error. Please try again!')
}
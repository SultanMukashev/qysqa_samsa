import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { GetTopicResponse } from "./type";

export default async function getTopic (id: number): Promise<ApiResponseMessage<GetTopicResponse>> {
  try{
    const response = await api.get<GetTopicResponse>(`/students/lessons/${id}`)

    return {
      ok: true,
      data: response.data,
      message: 'Lesson returned successfully!'
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
import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { GetTopicResponse } from "./type";

export default async function getTopic (id: number): Promise<ApiResponseMessage<GetTopicResponse['data']>> {
  try{
    const response = await api.get<GetTopicResponse>(`/topic/${id}`)

    return {
      ok: true,
      data: response.data.data,
      message: response.data.message
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
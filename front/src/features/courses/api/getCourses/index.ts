import { ApiResponseMessage } from "@/shared/types";
import { GetCoursesResponse } from "./type";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";

export default async function getCourses (): Promise<ApiResponseMessage<GetCoursesResponse['data']>> {
  try{
    const response = await api.get<GetCoursesResponse>('/courses')

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
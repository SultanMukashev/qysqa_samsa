import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { GetMyCoursesResponse } from "./type";

export default async function getMyCoursesTeacher (): Promise<ApiResponseMessage<GetMyCoursesResponse>> {

  try{
    const response = await api.get<GetMyCoursesResponse>('/teachers/courses/my')

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
import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { GetSingleCourseResponse } from "./type";

export default async function getSingleCourse (id: number): Promise<ApiResponseMessage<GetSingleCourseResponse>> {
  try{
    const response = await api.get<GetSingleCourseResponse>(`/students/courses/${id}`)

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
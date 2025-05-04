import { ApiResponseMessage } from "@/shared/types";
import api from "@/shared/api/useApi";
import { AxiosError } from "axios";
import { GetMyCourse } from "./type";

export default async function getMyCourse (id: number): Promise<ApiResponseMessage<GetMyCourse>> {
  try{
    const response = await api.get<GetMyCourse>(`/teachers/courses/my/${id}`)

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
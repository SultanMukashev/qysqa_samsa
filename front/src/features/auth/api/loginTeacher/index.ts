import api from "@/shared/api/useApi";
import { ApiResponseMessage } from "@/shared/types";
import { AxiosError } from "axios";
import { LoginTeacherRequest, LoginTeacherResponse } from "./type";

export async function loginTeacher (request: LoginTeacherRequest): Promise<ApiResponseMessage<LoginTeacherResponse>> {
  try{
    const response = await api.post<LoginTeacherResponse>('/teachers/auth', request)

    return {
      ok: true,
      data: response.data,
      message: 'Successfully loged in!'
    }
  } catch (error) {
    if (error instanceof AxiosError && error.response) {
      const message = error.response.data?.message || "Something went wrong!"
      return {
        ok: false,
        data: null,
        message: message
      }
    }
    throw new Error("Network error. Please try again.")
  }
}
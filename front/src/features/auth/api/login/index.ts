import api from "@/shared/api/useApi";
import { ApiResponseMessage } from "@/shared/types";
import { LoginRequest, LoginResponse } from "./type";
import { AxiosError } from "axios";

export async function login(
  request: LoginRequest
): Promise<ApiResponseMessage<LoginResponse>> {
  try {
    const response = await api.post<LoginResponse>("students/auth", request);

    return {
      ok: true,
      data: response.data,
      message: "Successfully loged in!",
    };
  } catch (error) {
    console.log(error)
    if (error instanceof AxiosError && error.response) {
      const message = error.response.data?.message || "Something went wrong!";
      return {
        ok: false,
        data: null,
        message: message,
      };
    }
    throw new Error("Network error. Please try again.");
  }
}

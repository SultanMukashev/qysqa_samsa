import api from "@/shared/api/useApi";

export async function amITeacher (): Promise<boolean> {
  try{
    const response = await api.get<boolean>('/teachers/am')

    return response.data
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  } catch (error) {
      return false
  }
}
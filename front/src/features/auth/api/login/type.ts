export type LoginRequest = {
  student_id: string,
  password: string
}

export type LoginResponse = {
  user_id: number,
  name: string,
  surname: string
}
export type LoginTeacherRequest = {
  id: number,
  password: string
}

export type LoginTeacherResponse = {
  user_id: number,
  name: string,
  surname: string
}
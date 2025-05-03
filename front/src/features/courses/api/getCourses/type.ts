export type GetCoursesResponse = {
  message: string,
  data: {
    id: number,
    title: string,
    description: string
  }[]
}
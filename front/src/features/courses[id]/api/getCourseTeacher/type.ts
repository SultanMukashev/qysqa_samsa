export type GetMyCourse = {
  course_id: number,
  name: string,
  description: string,
  lessons: {
    lesson_id: number,
    name: string,
    content: string
  }[]
}
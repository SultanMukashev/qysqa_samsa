export type GetSingleCourseResponse = {
  course_id: number,
  name: string,
  teacher: string,
  description: string,
  lessons: {
    lesson_id: number,
    name: string,
    content: string
  }[]
}
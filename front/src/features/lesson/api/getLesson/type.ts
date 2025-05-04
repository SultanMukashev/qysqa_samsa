export type GetTopicResponse = {
  lesson_id: number,
  title: string,
  conspect: string,
  content_file_url: string,
  course: {
    course_id: number,
    name: string,
    description: string
  }
}
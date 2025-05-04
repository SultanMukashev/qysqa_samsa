export type GetTopicResponse = {
  message: string,
  data:  {
    id: number,
    title: string,
    description: string,
    files: {
      id: number,
      url: string,
      name: string,
      type: string
    }[],
    notes: string
  }
}
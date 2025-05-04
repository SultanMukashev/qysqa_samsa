import LessonUI from "@/features/lesson/page"

export default async function LessonPage({ params }: { params: { id: string } }) {
  const id = parseInt(params.id, 10)

  return <LessonUI id={id} />
}

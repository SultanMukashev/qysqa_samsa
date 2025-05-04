import SingleCourseUI from "@/features/courses[id]/page"

const SingleCourse = ({
  params,
}: {
  params: { id: string }
}) => {
  const id = parseInt(params.id, 10)

  return <SingleCourseUI id={id} />
}

export default SingleCourse
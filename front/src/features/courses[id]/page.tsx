'use client'

import { useCourse } from "./store"
import { useEffect } from "react"
import { GetSingleCourseResponse } from "./api/type"

const SingleCourseUI = ({ id }: { id: number }) => {
  const { course, fetchCourse } = useCourse()

  useEffect(() => {
    fetchCourse(id)
  }, [id])

  return (
    <div className="flex flex-col gap-3">
      <div>
        <h1 className="font-bold text-3xl">{course?.name}</h1>
        <span className="text-sm text-neutral-400">{course?.description}</span>
      </div>
      <div className="flex flex-col gap-3 p-5">
        {course?.lessons.map((lesson: GetSingleCourseResponse['lessons'][0]) => (
          <a className="flex flex-col border rounded-xl p-3 border-neutral-200" href={`/courses/${lesson.lesson_id}`} key={lesson.lesson_id}>
            <label
              className="text-lg font-bold"
            >
              {lesson.name}
            </label>
            <span className="text-sm text-neutral-400">{lesson.content}</span>
          </a>
        ))}
      </div>
    </div>
  )
}

export default SingleCourseUI

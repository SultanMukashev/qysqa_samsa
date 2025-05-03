'use client'

import { useCourses } from "./store"
import { useEffect } from "react"
import { useRouter } from "next/navigation"

const CoursesUI = () => {
  const { courses, fetchCourses } = useCourses()
  const router = useRouter()

  useEffect(() => {
    fetchCourses()
  }, [])
  return(
    <div className="flex flex-col gap-3">
      <div>
        <h1 className="font-bold text-3xl">My Courses</h1>
        <span className="text-sm text-neutral-400">Welcome back! Let&apos;s continue learning</span>
      </div>
      <div className="flex flex-col gap-3">
        {courses?.map((course) => (
          <div key={course.id}>
            <label className="text-lg font-md" onClick={() => router.push(`/courses/${course.id}`)}>{course.title}</label>
            <span className="text-sm text-neutral-400">{course.description}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default CoursesUI
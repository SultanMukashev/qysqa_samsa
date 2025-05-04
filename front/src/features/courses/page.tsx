'use client'

import { useCourses } from "./store"
import { useEffect } from "react"

const CoursesUI = () => {
  const { courses, fetchCourses } = useCourses()

  useEffect(() => {
    fetchCourses()
  }, [])
  return(
    <div className="flex w-full flex-col gap-5">
      <div>
        <h1 className="font-bold text-3xl">My Courses</h1>
        <span className="text-sm text-neutral-400">Welcome back! Let&apos;s continue learning</span>
      </div>
      <div className="flex flex-col gap-3">
        {courses?.map((course) => (
          <div className="flex flex-row justify-between border rounded-xl border-neutral-200 p-4" key={course.course_id}>
            <div className="flex flex-col">
              <a href={`/courses/${course.course_id}`} className="text-lg font-bold" >{course.name}</a>
              <span className="text-sm text-neutral-400">{course.description}</span>
            </div>
            <img className="w-[350px] h-[240px] rounded-xl" src={'https://moodle.sdu.edu.kz/pluginfile.php/1/theme_alpha/defaultcourseimg/1745830895/IMG_8941%20%281%29%20%281%29.jpg'} />
          </div>
        ))}
      </div>
    </div>
  )
}

export default CoursesUI
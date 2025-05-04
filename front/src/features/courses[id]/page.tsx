'use client'

import { useCourse } from "./store"
import { useEffect, useState } from "react"
import { GetSingleCourseResponse } from "./api/getCourse/type"
import { Dialog } from "primereact/dialog"

const SingleCourseUI = ({ id }: { id: number }) => {
  const { course, fetchCourse, createLesson, fetchMyCourseTeacher } = useCourse()
  const [visible, setVisible] = useState<boolean>(false)
  const [lessonName, setLessonName] = useState<string>('')

  const teacher = localStorage.getItem('teacher')

  useEffect(() => {
    if (teacher === 'true') fetchMyCourseTeacher(id) 
      else fetchCourse(id)
  }, [id])

  return (
    <div className="flex flex-col gap-3">
      <div>
        <h1 className="font-bold text-3xl">{course?.name}</h1>
        <span className="text-sm text-neutral-400">{course?.description}</span>
      </div>
      <div className="flex flex-col gap-3 p-5">
        {teacher === 'true' && <button onClick={() => setVisible(true)}  className="border w-[150px] p-2 rounded-md">Create Lesson</button>}
        {course?.lessons.map((lesson: GetSingleCourseResponse['lessons'][0]) => (
          <a className="flex flex-col border rounded-xl p-3 border-neutral-200" href={`/lesson/${lesson.lesson_id}`} key={lesson.lesson_id}>
            <label
              className="text-lg font-bold"
            >
              {lesson.name}
            </label>
            <span className="text-sm text-neutral-400">{lesson.content}</span>
          </a>
        ))}
      </div>
      <Dialog header="Create Lesson" visible={visible} onHide={() => {if (!visible) return; setVisible(false); }}>
        <input className="p-3 border border-neutral-200 rounded-md" value={lessonName} onChange={(e) => setLessonName(e.target.value)}></input>
        <button className="p-3 border border-neutral-200 rounded-md" onClick={() => createLesson({title: lessonName, course_id: id})}>Create</button>
      </Dialog>
    </div>
  )
}

export default SingleCourseUI

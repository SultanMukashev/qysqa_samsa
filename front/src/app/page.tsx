'use client'

import CoursesUI from "@/features/courses/page"

export default function Home() {
  return (
    <div className="w-full flex justify-center items-center touch-none overflow-auto">
      <div className="w-7/8 p-2">
        <CoursesUI></CoursesUI>
      </div>
    </div>
  )
}

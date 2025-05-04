'use client'

import { useEffect } from "react"
import { useTopic } from "./store"
import { getFileIcon } from "@/shared/utils"

type TopicUIProps = {
  id: number
  contentHtml: string
}

const TopicUI = ({ id, contentHtml }: TopicUIProps) => {
  const { topic, fetchTopic } = useTopic()

  useEffect(() => {
    fetchTopic(id)
  }, [id])

  return (
    <div className="flex flex-col gap-3">
      <div>
        <h1 className="font-bold text-3xl">{topic?.title}</h1>
        <span className="text-sm text-neutral-400">{topic?.description}</span>
      </div>

      <div className="flex flex-col gap-3">
        <span className="text-md font-bold">Lesson Materials:</span>
        <div className="flex gap-3 flex-wrap">
          {topic?.files?.map((file) => (
            <a
              key={file.id}
              href={file.url}
              target="_blank"
              rel="noopener noreferrer"
              className="p-3 border rounded-md hover:bg-neutral-100 transition-colors w-40 flex flex-col items-start gap-2"
            >
              <div>{getFileIcon(file.type)}</div>
              <div className="font-medium text-sm line-clamp-1">{file.name}</div>
              <div className="text-xs text-neutral-500 capitalize">{file.type}</div>
            </a>
          ))}
        </div>
      </div>

      <div className="flex flex-col gap-3">
        <span className="text-md font-bold">Lecture Note:</span>
        <div className="prose max-w-none" dangerouslySetInnerHTML={{ __html: contentHtml }} />
      </div>
    </div>
  )
}

export default TopicUI

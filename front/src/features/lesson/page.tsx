'use client'

import { useEffect, useState } from "react"
import { useTopic } from "./store"
import { Send } from "lucide-react"
import { marked } from "marked"
import Prism from "prismjs"
import "prismjs/themes/prism.css"
import "prismjs/components/prism-javascript"
import "prismjs/components/prism-typescript"
import "prismjs/components/prism-jsx"
import "prismjs/components/prism-tsx"

interface Message {
  role: 'user' | 'ai'
  text: string
}

marked.setOptions({
  highlight: (code, lang) => {
    if (lang && Prism.languages[lang]) {
      return Prism.highlight(code, Prism.languages[lang], lang)
    }
    return code
  },
  breaks: true,
  gfm: true, 
})

const LessonUI = ({ id }: { id: number }) => {
  const { lesson, fetchLesson, uploadLesson, fet } = useTopic()
  const [contentHtml, setContentHtml] = useState<string>('')
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [file, setFile] = useState<File | null>(null)
  const teacher = localStorage.getItem('teacher')
  const me = localStorage.getItem('me')

  useEffect(() => {
    fetchLesson(id)
  }, [id, fetchLesson])

  useEffect(() => {
    if (lesson?.conspect) {
      const html = marked.parse(lesson.conspect)
      setContentHtml(html)
      // Highlight code blocks after DOM update
      setTimeout(() => {
        Prism.highlightAll()
      }, 0)
    }
  }, [lesson?.conspect])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMsg: Message = { role: 'user', text: input }
    setMessages((prev) => [...prev, userMsg])
    setInput("")
    setIsLoading(true)

    try {
      const res = await fetch("http://18.157.112.83:8082/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: input }),
      })

      if (!res.ok) throw new Error('Network response was not ok')

      const data = await res.json()
      console.log(data)
      const aiMsg: Message = { role: 'ai', text: data.answer ?? 'Sorry, I could not process your request.' }
      setMessages((prev) => [...prev, aiMsg])
    } catch (error) {
      console.error('Error:', error)
      setMessages((prev) => [...prev, { role: 'ai', text: "Sorry, an error occurred while processing your request." }])
    } finally {
      setIsLoading(false)
      // Highlight any code in new messages
      setTimeout(() => {
        Prism.highlightAll()
      }, 0)
    }
  }

  return (
    <div className="flex flex-col md:flex-row justify-between gap-6">
      {/* Lesson content */}
      <div className="flex flex-col gap-4 w-full md:w-2/3">
        <h1 className="font-bold text-3xl">{lesson?.title}</h1>

        {lesson?.content_file_url && (
          <a
            href={lesson.content_file_url}
            target="_blank"
            rel="noopener noreferrer"
            className="p-3 border rounded-md hover:bg-neutral-100 dark:hover:bg-neutral-800 transition-colors w-40"
          >
            Lesson Material
          </a>
        )}

      { lesson?.conspect && <div className="mt-4">
          <span className="text-md font-bold">Lecture Note:</span>
          <article
            className="markdown-body mt-2" 
            dangerouslySetInnerHTML={{ __html: contentHtml }}
          />
        </div>}
        {!lesson?.conspect && teacher === 'true' && (
        <div className="mt-4">
          <span className="text-md font-bold mb-2 block">Upload Lecture Materials</span>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="mb-2"
          />
          <button
            onClick={async () => {
              if (!file) return alert("Please select a file first.")
              const formData = new FormData()
              formData.append("file", file)

              try {
                const res = await fetch(`http://192.168.20.144:8000/teachers/lessons/${id}/upload`, {
                  headers: {
                    'Auth': me && JSON.parse(me).user_id
                  },
                  method: "POST",
                  body: formData, 
                })
                if (!res.ok) throw new Error("Upload failed")
                alert("Material uploaded successfully.")
              } catch (err) {
                console.error(err)
                alert("Failed to upload material.")
              } finally {
                setFile(null)
              }
            }}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Upload
          </button>

        </div>
      )}

      </div>

      {/* Chat UI */}
      <div className="flex flex-col w-full md:w-1/3 border rounded-xl p-4 h-[600px] bg-white dark:bg-neutral-900 shadow-sm">
        <h2 className="font-semibold text-xl mb-2">Ask AI</h2>

        <div className="flex-1 overflow-y-auto space-y-3 pr-1">
        {messages.map((msg, i) => (
          msg.role === 'ai' ? (
            <div
              key={i}
              className="rounded-lg px-3 py-2 max-w-[85%] text-sm bg-neutral-100 dark:bg-neutral-800"
              dangerouslySetInnerHTML={{ __html: marked.parse(msg.text) }}
            />
          ) : (
            <div
              key={i}
              className="rounded-lg px-3 py-2 max-w-[85%] text-sm bg-blue-100 dark:bg-blue-900 ml-auto text-right"
            >
              {msg.text}
            </div>
          )
        ))}

          {isLoading && (
            <div className="bg-neutral-100 dark:bg-neutral-800 rounded-lg px-3 py-2 max-w-[85%]">
              <div className="animate-pulse">Thinking...</div>
            </div>
          )}
        </div>

        <form
          className="flex items-center gap-2 pt-3 border-t mt-2"
          onSubmit={(e) => {
            e.preventDefault()
            handleSend()
          }}
        >
          <input
            className="flex-1 border rounded-lg px-3 py-2 text-sm outline-none bg-white dark:bg-neutral-800 dark:border-neutral-700"
            placeholder="Ask about this lesson..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="p-2 text-blue-600 hover:text-blue-800 dark:text-blue-400 dark:hover:text-blue-300"
            disabled={isLoading}
          >
            <Send className="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
  )
}

export default LessonUI
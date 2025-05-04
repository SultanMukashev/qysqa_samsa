import TopicUI from "@/features/topic/page"
import { parseMarkdown } from "@/shared/utils/parseMarkdown"
import fs from 'fs'
import path from 'path'

export default async function TopicPage({ params }: { params: { id: string } }) {
  const id = parseInt(params.id, 10)

  const markdownPath = path.join(process.cwd(), 'content', `topic-${id}.md`)
  let contentHtml = ''

  try {
    const markdown = fs.readFileSync(markdownPath, 'utf-8')
    contentHtml = await parseMarkdown(markdown)
  } catch (e) {
    console.warn(`Markdown file for topic ${id} not found. ${e}`)
  }

  return( <TopicUI id={id} contentHtml={contentHtml} />)
}

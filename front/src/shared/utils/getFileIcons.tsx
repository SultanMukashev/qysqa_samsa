import {
  FileText,
  FileImage,
  FileVideo,
  FileArchive,
  FileAudio,
  FileCode,
  FileSpreadsheet,
  FileBarChart,
  File,
} from "lucide-react"

export const getFileIcon = (type: string) => {
  switch (type.toLowerCase()) {
    case "pdf":
      return <FileText className="w-6 h-6 text-red-500" />
    case "image":
    case "jpg":
    case "png":
    case "jpeg":
      return <FileImage className="w-6 h-6 text-blue-400" />
    case "video":
    case "mp4":
      return <FileVideo className="w-6 h-6 text-purple-400" />
    case "zip":
    case "rar":
      return <FileArchive className="w-6 h-6 text-yellow-500" />
    case "audio":
    case "mp3":
      return <FileAudio className="w-6 h-6 text-green-500" />
    case "code":
    case "js":
    case "ts":
    case "html":
    case "css":
      return <FileCode className="w-6 h-6 text-indigo-500" />
    case "xls":
    case "xlsx":
      return <FileSpreadsheet className="w-6 h-6 text-green-600" />
    case "csv":
      return <FileBarChart className="w-6 h-6 text-orange-400" />
    case "doc":
    case "docx":
      return <FileText className="w-6 h-6 text-blue-600" />
    default:
      return <File className="w-6 h-6 text-neutral-400" />
  }
}

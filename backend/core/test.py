from core.processing.s3processor import S3FileProcessor
from core.generator.conspect import TextSummarizer
from core.generator.test import TestGenerator

import os
from dotenv import load_dotenv
load_dotenv()

processor = S3FileProcessor(bucket_name="contents",
                            aws_access_key='samsas3',
                            aws_secret_key='samsapass',
                            endpoint_url='http://46.101.215.10:9000')

text = processor.get_file_text("linux/Linux_Week5_Managing User Accounts.pptx")

syllabus = processor.get_file_text("linux/Linux 2025.docx")
# Send to summarizer
summarizer = TextSummarizer(api_key=os.getenv("OPENAI_API_KEY"))
# summary = summarizer.summarize(text)

generator = TestGenerator(api_key=os.getenv("OPENAI_API_KEY"))

questions = generator.generate_questions(topic_content=syllabus)

feedback = generator.generate_summary(topic_title="Syllabus of the Linux administration course", questions_with_answers="""[
  {
    "question": "What is the main focus of the course Linux Administration?",
    "selected_answer": "A. Windows operating system",
    "correct_answer": "C. Linux operating system"
  },
  {
    "question": "Which distributions of Linux are emphasized in the course?",
    "selected_answer": "B. Ubuntu and Fedora",
    "correct_answer": "A. RedHat and Debian"
  },
  {
    "question": "What core concepts of Linux are covered in the course?",
    "selected_answer": "C. Software management, security aspects",
    "correct_answer": "D. All of the above"
  },
  {
    "question": "What is the consequence of poor attendance in the course?",
    "selected_answer": "D. Penalty",
    "correct_answer": "B. Failure"
  },
  {
    "question": "What is the recommended book for the course Linux Administration?",
    "selected_answer": "C. RHCSA 8",
    "correct_answer": "A. Linus Essentials for Cybersecurity"
  }
]
""")

print(questions)
print()

print(feedback)
new_questions = generator.generate_questions(topic_content=text, progress_summary=feedback, previous_questions=questions, num_questions=10)
print()
print(new_questions)
# print(summary)


from s3processor import S3FileProcessor
from s3processor import TextSummarizer

import os
from dotenv import load_dotenv
load_dotenv()

processor = S3FileProcessor(bucket_name="contents",
                            aws_access_key='samsas3',
                            aws_secret_key='samsapass',
                            endpoint_url='http://46.101.215.10:9000')

text = processor.get_file_text("linux/Linux 2025.docx")
# Send to summarizer
summarizer = TextSummarizer(api_key=os.getenv("OPENAI_API_KEY"))
summary = summarizer.summarize(text)

print(summary)

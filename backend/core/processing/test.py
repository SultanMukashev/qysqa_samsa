from backend.processing.s3processor import S3FileProcessor
processor = S3FileProcessor(bucket_name="contents",
                            aws_access_key='samsas3',
                            aws_secret_key='samsapass',
                            endpoint_url='http://46.101.215.10:9000')
summary = processor.process_and_summarize("linux/Linux 2025.docx")
print(summary)

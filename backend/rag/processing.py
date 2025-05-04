from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.processing.s3processor import S3FileProcessor
from langchain.schema import Document  # assuming your class is in this file

def load_and_split_documents_from_s3(bucket_name, s3_prefix="", endpoint_url=None,
                                     aws_access_key=None, aws_secret_key=None,
                                     chunk_size=1000, chunk_overlap=200):
    print("Initializing S3 processor...")
    processor = S3FileProcessor(
        bucket_name=bucket_name,
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
        endpoint_url=endpoint_url
    )

    print("Listing S3 files...")
    s3_objects = processor.s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_prefix).get('Contents', [])
    supported_files = [obj['Key'] for obj in s3_objects if obj['Key'].lower().endswith(('.pdf', '.docx', '.pptx', '.txt'))]

    if not supported_files:
        print("No supported files found in S3.")
        return []

    print(f"Found {len(supported_files)} supported files.")

    full_docs = []
    for key in supported_files:
        try:
            print(f"Processing file: {key}")
            text = processor.get_file_text(key)
            if text.strip():
                full_docs.append({"source": key, "text": text})
        except Exception as e:
            print(f"Error processing {key}: {e}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False
    )

    split_docs = []
    for doc in full_docs:
        chunks = splitter.split_text(doc["text"])
        for i, chunk in enumerate(chunks):
            split_docs.append(Document(
            page_content=chunk,
            metadata={"source": doc["source"], "chunk_index": i}
        ))

    return split_docs

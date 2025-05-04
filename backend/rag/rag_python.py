import os
import time
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from prompts import SDU_BOT_PROMPT_TEMPLATE

from config import VECTOR_STORE_DIR, OPENAI_API_KEY
from models import openai_llm
from retrievers import setup_retrievers
from processing import load_and_split_documents_from_s3
from utils import count_tokens, calculate_cost, print_token_breakdown

load_dotenv()

# Создание директории для векторного хранилища
if not os.path.exists(VECTOR_STORE_DIR):
    print(f"Creating vector store directory at {VECTOR_STORE_DIR}")
    os.makedirs(VECTOR_STORE_DIR)
# Загрузка и обработка документов
start_time = time.time()
split_docs = load_and_split_documents_from_s3(bucket_name="contents",
                            aws_access_key='samsas3',
                            aws_secret_key='samsapass',
                            endpoint_url='http://46.101.215.10:9000',
                            s3_prefix="linux"
                            )

# Настройка ретриверов
compression_pipeline, vectorstore = setup_retrievers(split_docs)

# Проверка и заполнение векторного хранилища
if len(vectorstore.get()['ids']) == 0:
    print("Vector store is empty. Adding documents...")
    vectorstore.add_documents(split_docs)
    print("Documents added to vector store.")
else:
    print("Using existing vector store.")

# Вывод времени обработки
execution_time = time.time() - start_time
print(f"\nDocument processing time: {execution_time:.2f} seconds")

# Инициализация памяти для диалога
memory = ConversationBufferMemory(
    memory_key="chat_history",
    input_key="question",
    output_key="answer",
    return_messages=True
)

# /openai_llm.api_key=OPENAI_API_KEY

# Создание цепочки для ответов
qa_chain = ConversationalRetrievalChain.from_llm(
    llm=openai_llm,
    retriever=compression_pipeline,
    memory=memory,
    return_source_documents=True,
    combine_docs_chain_kwargs={
        "prompt": SDU_BOT_PROMPT_TEMPLATE,
        "document_variable_name": "context",
        "document_separator": "\n\n"
    },
    verbose=False
)

def get_sdu_bot_response(query: str):
    llm_start_time = time.time()
    
    response = qa_chain.invoke({"question": query})
    answer = response['answer']
    source_docs = response['source_documents']
    
    llm_execution_time = time.time() - llm_start_time
    print(f"\nLLM Response Time: {llm_execution_time:.2f} seconds")

    context = "\n\n".join([doc.page_content for doc in source_docs])
    
    query_tokens = count_tokens(query)
    context_tokens = count_tokens(context)
    answer_tokens = count_tokens(answer)
    prompt_tokens = count_tokens(SDU_BOT_PROMPT_TEMPLATE.template)
    
    print_token_breakdown(query_tokens, context_tokens, prompt_tokens, answer_tokens)
    
    current_cost = calculate_cost(
        prompt_tokens + context_tokens + query_tokens,
        answer_tokens
    )

    return answer, current_cost

# def main():
#     print("SDU Bot: Hi! I'm your SDU assistant. Ask me anything about SDU in any language!")
#     print("(Type 'exit' to end the conversation)")

#     total_session_cost = 0.0

#     while True:
#         try:
#             question = input("\nYour question: ").strip()
            
#             if not question:
#                 print("Please enter a question.")
#                 continue
            
#             if question.lower() == "exit":
#                 print("\nSession Summary:")
#                 print("-" * 50)
#                 print(f"Total session cost: ${total_session_cost:.6f}")
#                 print("\nSDU Bot: Goodbye! Feel free to ask me questions about SDU!")
#                 break
            
#             answer, current_cost = get_sdu_bot_response(question)
#             print("\nSDU Bot's Response:")
#             print("-" * 50)
#             print(answer)
            
#             total_session_cost += current_cost
#             print(f"Current session cost: ${current_cost:.6f}")
            
#         except KeyboardInterrupt:
#             print("\n\nSession interrupted by user.")
#             break
#         except Exception as e:
#             print(f"\nUnexpected error: {str(e)}")
#             print("Please try again with a different question.")

# if __name__ == "__main__":
#     main()
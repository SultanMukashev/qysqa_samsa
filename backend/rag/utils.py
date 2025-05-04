import time
import tiktoken
from config import TOKEN_MODEL, INPUT_COST_PER_1M, OUTPUT_COST_PER_1M

def count_tokens(text: str, model: str = TOKEN_MODEL) -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def calculate_cost(input_tokens: int, output_tokens: int, model: str = TOKEN_MODEL) -> float:
    input_cost = (input_tokens / 1_000_000) * INPUT_COST_PER_1M
    output_cost = (output_tokens / 1_000_000) * OUTPUT_COST_PER_1M
    return input_cost + output_cost

def pretty_print_docs(docs):
    print(
        f"\n{'-' * 100}\n".join([f"Document {i+1}:\n\n + {d.page_content}" for i,d in enumerate(docs)])
    )

def print_token_breakdown(query_tokens, context_tokens, prompt_tokens, answer_tokens):
    print(f"Token breakdown:")
    print(f"- Query tokens: {query_tokens}")
    print(f"- Context tokens: {context_tokens}")
    print(f"- Prompt template tokens: {prompt_tokens}")
    print(f"- Total input tokens: {prompt_tokens + context_tokens + query_tokens}")
    print(f"- Answer tokens: {answer_tokens}") 
class TextSummarizer:
    def __init__(self, api_key, model='gpt-3.5-turbo'):
        import openai
        self.openai = openai
        self.openai.api_key = api_key
        self.model = model

    def summarize(self, text):
        # Replace this with your actual LLM API
        import openai
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Or gpt-4, etc.
            messages=[
                {"role": "system", "content": "Create readable and informative conspect from the following document so student will understand everything, make it raw markdown:"},
                {"role": "user", "content": text}
            ],
            # max_tokens=max_tokens,
            temperature=0,
        )
        return response.choices[0].message.content
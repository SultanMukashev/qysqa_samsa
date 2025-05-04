class TestGenerator:
    def __init__(self):
        import openai
        self.openai = openai
        self.openai.api_key = 'OAI_KEY'
        self.model = 'gpt-3.5-turbo'

    def generate_questions(self, topic_content, progress_summary=None ,previous_questions=None, num_questions=5, question_type="mixed"):
        """
        Generate questions based on topic content and student progress.

        :param topic_content: String. Lecture or topic material.
        :param progress: Dict. Should contain 'weak_topics', 'strengths', 'completed', etc.
        :param num_questions: Int. Number of questions to generate.
        :param question_type: "mcq", "short", or "mixed".
        """
        # Compose prompt
        prompt = f"""You are a helpful assistant that creates educational quizzes.

Generate {num_questions} {question_type.upper()} Student is currently progressing through the course.

Previous Questions:
{previous_questions}

Here is their recent performance summary:
{progress_summary}
Based on the content below, generate a quiz that contains some question sugestions from previous topics while evaluating new concepts.
Generate a quiz that includes:
- 20% questions from the previous topic(s)
- 80% new questions based on the current topic content
Content:
{topic_content}

Respond in JSON with the format:
[
  {{
    "question": "string",
    "options": ["a", "b", "c", "d"],  // Only for MCQs
    "answer": "correct answer"
  }},
  ...
]
Topic Content:
{topic_content[:4000]}"""  # Limit to fit token budget

        # Call OpenAI
        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        print(prompt)
        import json
        try:
            return json.loads(response.choices[0].message.content)
        except json.JSONDecodeError:
            return [{"error": "Failed to parse questions from model response."}]


    def generate_summary(self, topic_title, questions_with_answers):
        """
        Generates a summary of the student's performance on a quiz.
        :param topic_title: Topic name (e.g., "Linux /etc/shadow file")
        :param questions_with_answers: List of dicts with:
            - question
            - selected_answer
            - correct_answer
        """
        prompt = f"""You are an educational assistant that summarizes quiz performance.

Topic: {topic_title}

Student has completed a quiz. Based on their answers below, evaluate their understanding. 
Mention what was done well and what needs improvement. Provide a short summary of their weak points and what needs to be included in next test.

Quiz Results (JSON):
{questions_with_answers}

Respond in plain text summary.
"""

        response = self.openai.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        return response.choices[0].message.content.strip()

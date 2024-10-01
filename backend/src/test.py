from dotenv import load_dotenv
from openai import OpenAI
import os
from textwrap import dedent
from pydantic import BaseModel

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

MODEL = "gpt-4o-2024-08-06"

math_tutor_prompt = '''
    You are a helpful math tutor. You will be provided with a math problem,
    and your goal will be to output a step by step solution, along with a final answer.
    For each step, just provide the output as an equation use the explanation field to detail the reasoning.
'''

class MathReasoning(BaseModel):
    class Step(BaseModel):
        explanation: str
        output: str

    steps: list[Step]
    final_answer: str

def get_math_solution(question: str):
    completion = client.beta.chat.completions.parse(
        model=MODEL,
        messages=[
            {"role": "system", "content": dedent(math_tutor_prompt)},
            {"role": "user", "content": question},
        ],
        response_format=MathReasoning,
    )

    return completion.choices[0].message

# Testing with an example question
question = "how can I solve 8x + 7 = -23"

result = get_math_solution(question).parsed

print(result.steps)
print("Final answer:")
print(result.final_answer)
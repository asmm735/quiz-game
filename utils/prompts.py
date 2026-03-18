"""
Well-engineered prompts for Google Gemini API.
These prompts are specifically crafted to get reliable JSON responses from Gemini.
"""

def get_explain_concept_prompt(topic: str, question: str = None) -> str:
    """Simplified prompt for fast, reliable explanations."""
    return f"""Explain "{topic}" simply. Respond ONLY as valid JSON with NO extra text:
{{
    "simple_explanation": "2-3 sentence beginner explanation using everyday language",
    "real_world_analogy": "A real-world analogy that makes this relatable",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "follow_up_question": "A simple question to check understanding",
    "fun_fact": "An interesting fact related to {topic}"
}}"""


def get_quiz_generation_prompt(topic: str, difficulty: str, num_questions: int) -> str:
    """Quiz generation prompt with complete examples and strict requirements."""
    return f"""Create EXACTLY {num_questions} {difficulty} quiz questions about "{topic}".

REQUIREMENTS:
- REAL questions with complete, detailed content (not generic templates)
- All answers must be FACTUALLY CORRECT - verify every answer
- Each option must be full text, unique, and plausible
- correct_answer_index points to the ONE correct option (0, 1, 2, or 3)
- explanation explains WHY that answer is correct

EXAMPLE (return similar format):
{{
  "topic": "Python Programming",
  "difficulty": "easy",
  "questions": [
    {{
      "id": 1,
      "question": "What does the len() function return?",
      "options": ["The first element of a list", "The number of items in an object like a list or string", "The data type of an object", "The memory address of an object"],
      "correct_answer_index": 1,
      "explanation": "The len() function returns the number of items in a sequence (list, string, tuple) or the number of key-value pairs in a dictionary."
    }},
    {{
      "id": 2,
      "question": "Which of these is a mutable data type in Python?",
      "options": ["Tuple", "String", "List", "Integer"],
      "correct_answer_index": 2,
      "explanation": "Lists are mutable (can be modified), while tuples, strings, and integers are immutable."
    }}
  ]
}}

NOW generate {num_questions} real questions about {topic}. Return ONLY valid JSON, no other text."""


def get_evaluate_answer_prompt(question: str, user_answer: str, correct_answer: str, options: list) -> str:
    """
    Prompt for evaluating a student's answer.
    """
    options_str = ", ".join(options)
    
    return f"""Evaluate a student's answer to this question.

Question: "{question}"
Available options: {options_str}
Student's answer: "{user_answer}"
Correct answer: "{correct_answer}"

Your response MUST be ONLY valid JSON, nothing else:

{{
    "is_correct": true or false,
    "score": a number from 0-100,
    "explanation": "Clear explanation of whether the answer is correct or not, and why.",
    "improvement_tip": "Specific advice on how the student can improve their understanding.",
    "similar_concept": "A related concept or topic the student should learn next."
}}

IMPORTANT: Return ONLY valid JSON. No other text."""


def get_explain_wrong_answer_prompt(question: str, user_answer: str, correct_answer: str, explanation: str) -> str:
    """
    Prompt for deep explanation of why student got answer wrong.
    """
    return f"""A student got this question WRONG. Help them understand their mistake deeply.

Question: "{question}"
Their answer: "{user_answer}"
Correct answer: "{correct_answer}"
Why it's correct: "{explanation}"

Your response MUST be ONLY valid JSON, nothing else:

{{
    "misconception": "Identify the specific misconception or misunderstanding they had.",
    "correct_thinking": "Explain the correct way to think about this problem. Make it very clear.",
    "mnemonic_or_trick": "A memory trick, acronym, or mental model to remember this correctly.",
    "next_steps": "What related concepts or topics they should study to strengthen their understanding."
}}

IMPORTANT: Return ONLY valid JSON. No other text."""

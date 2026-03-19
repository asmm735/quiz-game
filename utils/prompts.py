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
    """Simplified quiz generation prompt for faster responses."""
    return f"""Create {num_questions} {difficulty} quiz questions about {topic}. Respond ONLY as valid JSON:
{{
  "topic": "{topic}",
  "difficulty": "{difficulty}",
  "questions": [
    {{
      "id": 1,
      "question": "The actual question text goes here?",
      "options": ["Option A - complete text", "Option B - complete text", "Option C - complete text", "Option D - complete text"],
      "correct_answer_index": 0,
      "explanation": "Why option A is correct and others are wrong."
    }}
  ]
}}

REQUIREMENTS:
- Real, specific questions about {topic} - not generic
- Complete answer text (not A, B, C, D)
- correct_answer_index: 0, 1, 2, or 3
- All answers factually correct
- No other text, only JSON"""


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

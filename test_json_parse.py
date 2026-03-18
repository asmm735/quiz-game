import requests
import json

# Test what Ollama actually returns for quiz
prompt = """Generate 2 easy multiple-choice quiz questions about Python Recursion ONLY as valid JSON:
{
    "topic": "Python Recursion",
    "difficulty": "easy",
    "questions": [
        {
            "id": 1,
            "question": "What is recursion?",
            "options": ["A function calling itself", "A loop statement", "A data structure", "A Python library"],
            "correct_answer_index": 0,
            "explanation": "Recursion is when a function calls itself."
        }
    ]
}"""

print("[TEST] Sending simplified prompt to Ollama...")
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "mistral", "prompt": prompt, "stream": False},
    timeout=180
)

raw = response.json().get("response", "")
print(f"\n[RAW RESPONSE] (first 800 chars):\n{raw[:800]}")
print(f"\n[LENGTH] Total: {len(raw)} chars")

# Try to extract JSON
try:
    text = raw.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    
    result = json.loads(text)
    print(f"\n[SUCCESS] Parsed JSON!")
    print(f"Questions: {len(result.get('questions', []))}")
    if result.get('questions'):
        q = result['questions'][0]
        print(f"Q1: {q.get('question')}")
        print(f"Options: {q.get('options')}")
except Exception as e:
    print(f"\n[FAIL] JSON parsing failed: {e}")
    print(f"Tried to parse: {text[:200]}")

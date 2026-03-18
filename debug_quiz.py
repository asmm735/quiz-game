from services.llm_service import LLMService
import json
import time

print("[TEST] Checking what Ollama is actually generating for quizzes...")
service = LLMService(use_demo_mode=False)

start = time.time()
result = service.generate_quiz_questions("SQL Database", "easy", 2)
elapsed = time.time() - start

print(f"\n[OK] Got quiz in {elapsed:.1f} seconds")
print(f"\n[RAW OUTPUT]:")
print(json.dumps(result, indent=2))

if result.get('questions'):
    for i, q in enumerate(result['questions'], 1):
        print(f"\n{'='*60}")
        print(f"Question {i}:")
        print(f"  Text: {q.get('question', 'N/A')}")
        print(f"  Options:")
        for j, opt in enumerate(q.get('options', []), 1):
            print(f"    {j}. {opt}")
        print(f"  Correct Index: {q.get('correct_answer_index', 'N/A')}")

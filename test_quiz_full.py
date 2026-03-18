from services.llm_service import LLMService
import time
import json

print("[TEST] Testing quiz generation with 180s timeout and simplified prompt...")
service = LLMService(use_demo_mode=False)

start = time.time()
result = service.generate_quiz_questions("Python Loops", "easy", 2)
elapsed = time.time() - start

print(f"\n[TIME] Generated in {elapsed:.1f} seconds")
print(f"[RESULT] Type: {type(result)}")
print(f"[RESULT] Keys: {list(result.keys())}")

if result.get('questions'):
    print(f"[SUCCESS] Got {len(result['questions'])} questions!")
    q = result['questions'][0]
    print(f"\nQ1: {q.get('question', '')}")
    print(f"Options:")
    for i, opt in enumerate(q.get('options', []), 1):
        print(f"  {i}. {opt}")
    print(f"Correct: Index {q.get('correct_answer_index')}")
else:
    print(f"[FAIL] No questions returned")
    print(f"Result: {json.dumps(result, indent=2)}")

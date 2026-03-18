from services.llm_service import LLMService
import time

print("[TEST] Testing with 300s timeout - requesting 5 questions...")
service = LLMService(use_demo_mode=False)

start = time.time()
result = service.generate_quiz_questions("Python Loops", "easy", 5)
elapsed = time.time() - start

print(f"\n[TIME] Generated in {elapsed:.1f} seconds")
print(f"[RESULT] Got {len(result.get('questions', []))} questions")

if result.get('questions'):
    for i, q in enumerate(result['questions'], 1):
        print(f"\nQ{i}: {q.get('question', '')[:80]}")
        print(f"  Options: {len(q.get('options', []))} choices")

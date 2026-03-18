from services.llm_service import LLMService
import time

print("[TEST 1] Testing explain_concept with simplified prompt...")
service = LLMService(use_demo_mode=False)

start = time.time()
result = service.explain_concept("Python Loops")
elapsed = time.time() - start
print(f"[TIME] Got explanation in {elapsed:.1f} seconds")
print(f"[SAMPLE] {result.get('simple_explanation', '')[:100]}\n")

print("[TEST 2] Testing same topic again (should use CACHE)...")
start2 = time.time()
result2 = service.explain_concept("Python Loops")
elapsed2 = time.time() - start2
print(f"[TIME] Cache retrieval: {elapsed2:.3f} seconds (should be instant)")

print("\n[TEST 3] Testing quiz generation with simplified prompt...")
start = time.time()
result = service.generate_quiz_questions("Python", "easy", 2)
elapsed = time.time() - start
print(f"[TIME] Generated quiz in {elapsed:.1f} seconds")

if result.get('questions'):
    q = result['questions'][0]
    print(f"[SAMPLE] Q: {q.get('question', '')[:80]}")
    print(f"[SAMPLE] Options: {len(q.get('options', []))} choices")
    print(f"[SAMPLE] Opt 1: {q.get('options', [''])[0][:60]}")

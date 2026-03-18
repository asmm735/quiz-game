from services.llm_service import LLMService
import time

print("[TEST] Testing quiz generation with Ollama...")
service = LLMService(use_demo_mode=False)

start = time.time()
result = service.generate_quiz_questions("Python Functions", "easy", 3)
elapsed = time.time() - start

print(f"\n[OK] Got quiz in {elapsed:.1f} seconds")
print(f"[OK] Topic: {result.get('topic', 'N/A')}")
print(f"[OK] Difficulty: {result.get('difficulty', 'N/A')}")
print(f"[OK] Number of Questions: {len(result.get('questions', []))}")

questions = result.get('questions', [])
if questions:
    print(f"\n[SAMPLE] First Question:")
    print(f"  Q: {questions[0].get('question', 'N/A')}")
    print(f"  Options: {questions[0].get('options', [])}")
    print(f"  Correct Index: {questions[0].get('correct_answer_index', 'N/A')}")
    print(f"  Explanation: {questions[0].get('explanation', 'N/A')[:100]}")

from services.llm_service import LLMService
import time

print("[TEST] Testing explain_concept with Ollama...")
service = LLMService(use_demo_mode=False)
start = time.time()
result = service.explain_concept("Python Lists")
elapsed = time.time() - start
print(f"\n[OK] Got response in {elapsed:.1f} seconds")
print(f"[OK] Keys: {list(result.keys())}")
print(f"[SAMPLE] Explanation: {result.get('simple_explanation', '')[:150]}")

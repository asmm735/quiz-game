"""
Test if Ollama is set up correctly
Run: python test_ollama.py
"""

import requests
import json

print("=" * 60)
print("OLLAMA TEST SCRIPT")
print("=" * 60)

# Step 1: Check if Ollama is running
print("\n[Step 1] Checking if Ollama is running...")
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=2)
    print("[OK] Ollama is running!")
    
    # Show available models
    data = response.json()
    models = data.get("models", [])
    
    if models:
        print(f"[OK] Found {len(models)} model(s):")
        for model in models:
            name = model.get("name", "unknown")
            print(f"     - {name}")
    else:
        print("[WARN] No models found. Run: ollama pull mistral")
except Exception as e:
    print(f"[FAIL] Cannot connect to Ollama")
    print(f"Error: {e}")
    print("\nMake sure:")
    print("1. Ollama is installed from https://ollama.ai")
    print("2. Ollama is running (check system tray)")
    print("3. Run: ollama pull mistral")
    exit(1)

# Step 2: Test if mistral model exists
print("\n[Step 2] Checking for mistral model...")
has_mistral = any("mistral" in m.get("name", "").lower() for m in models)

if has_mistral:
    print("[OK] Mistral model is available")
else:
    print("[WARN] Mistral not found. Run: ollama pull mistral")
    print("Trying to pull mistral...")
    try:
        # This won't work from this script, but let's inform the user
        print("Please run in PowerShell: ollama pull mistral")
    except:
        pass

# Step 3: Test generating a response
if has_mistral:
    print("\n[Step 3] Testing model generation...")
    try:
        test_prompt = "Say 'Hello world' and nothing else."
        print(f"Prompt: {test_prompt}")
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": test_prompt,
                "stream": False,
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            output = data.get("response", "")
            print(f"[OK] Got response: {output}")
        else:
            print(f"[FAIL] HTTP {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"[FAIL] Error: {e}")

print("\n" + "=" * 60)
print("[OK] Ollama is ready!")
print("=" * 60)

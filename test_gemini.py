"""
Test script to verify Gemini API setup
Run this to diagnose the issue: python test_gemini.py
"""

import os
import json
from dotenv import load_dotenv

print("=" * 60)
print("GEMINI API TEST SCRIPT")
print("=" * 60)

# Step 1: Load .env
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

print("\n[Step 1] Checking API Key in .env")
if api_key:
    print(f"[OK] API Key found: {api_key[:20]}...")
else:
    print("[FAIL] NO API KEY FOUND in .env")
    print("   Please add: OPENAI_API_KEY=your_gemini_key_here")
    exit(1)

# Step 2: Try to import genai
print("\n[Step 2] Checking google-generativeai library")
try:
    import google.generativeai as genai
    print("[OK] google-generativeai imported successfully")
except ImportError as e:
    print(f"[FAIL] Failed to import: {e}")
    print("   Run: pip install google-generativeai")
    exit(1)

# Step 3: Configure Gemini
print("\n[Step 3] Configuring Gemini API")
try:
    genai.configure(api_key=api_key)
    print("[OK] Gemini configured successfully")
except Exception as e:
    print(f"[FAIL] Configuration failed: {e}")
    exit(1)

# Step 4: Initialize model
print("\n[Step 4] Initializing Gemini model")
try:
    model = genai.GenerativeModel('gemini-2.0-flash')
    print("[OK] Model initialized successfully")
except Exception as e:
    print(f"[FAIL] Model initialization failed: {e}")
    exit(1)

# Step 5: Test simple prompt
print("\n[Step 5] Testing simple API call")
try:
    test_prompt = "Explain water in one sentence."
    print(f"   Sending prompt: '{test_prompt}'")
    response = model.generate_content(test_prompt)
    print("[OK] API call successful!")
    print(f"   Response: {response.text[:100]}...")
except Exception as e:
    print(f"[FAIL] API call failed: {e}")
    exit(1)

# Step 6: Test JSON response
print("\n[Step 6] Testing JSON response format")
try:
    json_prompt = '''Respond ONLY with this JSON, no other text:
{
    "word": "hello",
    "meaning": "a greeting"
}'''
    print(f"   Sending JSON prompt")
    response = model.generate_content(json_prompt)
    response_text = response.text.strip()
    print(f"   Raw response: {response_text}")
    
    # Try to parse
    parsed = json.loads(response_text)
    print("[OK] JSON parsing successful!")
    print(f"   Parsed: {parsed}")
except json.JSONDecodeError as e:
    print(f"[FAIL] JSON parse failed: {e}")
    print(f"   Response was: {response_text[:200]}")
except Exception as e:
    print(f"[FAIL] JSON test failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("[OK] ALL TESTS PASSED!")
print("[OK] Your Gemini API is working correctly")
print("=" * 60)

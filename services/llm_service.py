"""Ollama LLM Service"""
import os, json, requests, hashlib
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv
from utils.prompts import *

load_dotenv()

class LLMService:
    def __init__(self, use_demo_mode=False):
        self.use_demo_mode = use_demo_mode
        self.client = None
        self.model_name = "mistral"
        self.ollama_host = "http://localhost:11434"
        self.cache = {}  # Response cache
        if not use_demo_mode:
            try:
                response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
                if response.status_code == 200:
                    print("[OK] Ollama running")
                    self.client = "ollama"
                else:
                    raise Exception("Not responding")
            except Exception as e:
                print(f"[FAIL] Ollama unavailable: {e}")
                self.use_demo_mode = True
    
    def _call_ollama(self, prompt: str) -> str:
        try:
            response = requests.post(
                f"{self.ollama_host}/api/generate",
                json={"model": self.model_name, "prompt": prompt, "stream": False},
                timeout=300
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            raise Exception(f"HTTP {response.status_code}")
        except requests.exceptions.Timeout:
            raise Exception("Ollama timed out after 300 seconds")
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        if not text:
            return None
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        try:
            return json.loads(text)
        except:
            return None
    
    def _get_cache_key(self, name: str, *args) -> str:
        """Generate cache key from function name and arguments."""
        key_str = f"{name}_{','.join(str(a) for a in args)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def explain_concept(self, topic: str, question: str = None) -> Dict:
        if self.use_demo_mode or not self.client:
            return self._demo_explain(topic)
        
        # Check cache
        cache_key = self._get_cache_key("explain", topic)
        if cache_key in self.cache:
            print(f"[CACHE] Returning cached explanation for {topic}")
            return self.cache[cache_key]
        
        try:
            prompt = get_explain_concept_prompt(topic, question)
            print(f"[INFO] Calling Ollama for: {topic}")
            response_text = self._call_ollama(prompt)
            result = self._extract_json(response_text)
            if result and "simple_explanation" in result:
                self.cache[cache_key] = result  # Store in cache
                print(f"[OK] Got Ollama response")
                return result
            return self._demo_explain(topic)
        except Exception as e:
            print(f"[FAIL] {e}")
            return self._demo_explain(topic)
    
    def _validate_quiz(self, quiz_data: Dict) -> bool:
        """Validate that quiz questions are well-formed and real (not placeholder)"""
        if not quiz_data or "questions" not in quiz_data:
            print("[VALIDATE] No questions field found")
            return False
        
        questions = quiz_data.get("questions", [])
        if not questions:
            print("[VALIDATE] Empty questions list")
            return False
        
        for i, q in enumerate(questions):
            # Check required fields
            required_fields = ["question", "options", "correct_answer_index", "explanation"]
            missing = [f for f in required_fields if f not in q]
            if missing:
                print(f"[VALIDATE] Question {i+1} missing fields: {missing}")
                return False
            
            # Check correct_answer_index is valid
            idx = q.get("correct_answer_index", -1)
            options = q.get("options", [])
            if not isinstance(idx, int) or idx < 0 or idx >= len(options):
                print(f"[VALIDATE] Question {i+1} invalid correct_answer_index: {idx} (options: {len(options)})")
                return False
            
            # Check options are non-empty and substantial
            if not options or len(options) < 2:
                print(f"[VALIDATE] Question {i+1} insufficient options: {len(options)}")
                return False
            
            for j, opt in enumerate(options):
                opt_str = str(opt).strip()
                if not opt_str:
                    print(f"[VALIDATE] Question {i+1} option {j} is empty")
                    return False
                # Reject single-letter options (A, B, C, D) - they should be full text
                if len(opt_str) == 1 and opt_str in "ABCD":
                    print(f"[VALIDATE] Question {i+1} option {j} is single letter: {opt_str}")
                    return False
            
            # Check question is not a template like "Q1 about topic?"
            q_text = q.get("question", "").lower().strip()
            if q_text.startswith("q") and q_text.endswith("?") and "about" in q_text:
                print(f"[VALIDATE] Question {i+1} looks like placeholder: {q_text}")
                return False
            
            # Check explanation exists and is meaningful
            explanation = str(q.get("explanation", "")).strip()
            if not explanation or len(explanation) < 5:
                print(f"[VALIDATE] Question {i+1} explanation too short: {len(explanation)}")
                return False
        
        print(f"[VALIDATE] All {len(questions)} questions passed validation")
        return True
    
    def generate_quiz_questions(self, topic: str, difficulty: str, num_questions: int) -> Dict:
        if self.use_demo_mode or not self.client:
            return self._demo_quiz(topic, difficulty, num_questions)
        
        # Check cache
        cache_key = self._get_cache_key("quiz", topic, difficulty, num_questions)
        if cache_key in self.cache:
            print(f"[CACHE] Returning cached quiz for {topic} ({difficulty})")
            return self.cache[cache_key]
        
        try:
            prompt = get_quiz_generation_prompt(topic, difficulty, num_questions)
            print(f"[INFO] Generating quiz for: {topic} ({difficulty})")
            response_text = self._call_ollama(prompt)
            
            result = self._extract_json(response_text)
            # Validate the quiz data
            if result and self._validate_quiz(result):
                questions = result.get("questions", [])
                if len(questions) > 0:
                    # Accept any number of questions generated
                    self.cache[cache_key] = result
                    print(f"[OK] Generated {len(questions)} valid questions")
                    return result
            
            # If validation fails, show warning and use demo
            print(f"[WARN] Quiz validation failed, using demo questions")
            return self._demo_quiz(topic, difficulty, num_questions)
        except Exception as e:
            print(f"[FAIL] Quiz generation: {e}")
            return self._demo_quiz(topic, difficulty, num_questions)
    
    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, options: List[str]) -> Dict:
        if self.use_demo_mode or not self.client:
            is_correct = user_answer.lower() == correct_answer.lower()
            return {"is_correct": is_correct, "score": 100 if is_correct else 30, "explanation": "Good", "improvement_tip": "Practice", "similar_concept": "Related"}
        try:
            prompt = get_evaluate_answer_prompt(question, user_answer, correct_answer, options)
            response_text = self._call_ollama(prompt)
            result = self._extract_json(response_text)
            if result and "is_correct" in result:
                return result
            return {"is_correct": False, "score": 0, "explanation": "Error", "improvement_tip": "Review", "similar_concept": "N/A"}
        except Exception as e:
            return {"is_correct": False, "score": 0, "explanation": "Error", "improvement_tip": "Review", "similar_concept": "N/A"}
    
    def explain_wrong_answer(self, question: str, user_answer: str, correct_answer: str, explanation: str) -> Dict:
        if self.use_demo_mode or not self.client:
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
        try:
            prompt = get_explain_wrong_answer_prompt(question, user_answer, correct_answer, explanation)
            response_text = self._call_ollama(prompt)
            result = self._extract_json(response_text)
            if result and "misconception" in result:
                return result
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
        except Exception as e:
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
    
    def _demo_explain(self, topic: str) -> Dict:
        return {"simple_explanation": f"{topic} is fundamental.", "real_world_analogy": f"Like learning {topic}.", "key_points": ["P1", "P2", "P3"], "follow_up_question": f"What is {topic}?", "fun_fact": f"Fun: {topic}!"}
    
    def _demo_quiz(self, topic: str, difficulty: str, num_questions: int) -> Dict:
        demo_questions = {
            "math": [
                {"id": 1, "question": "What is the derivative of x²?", "options": ["x", "2x", "x²", "2"], "correct_answer_index": 1, "explanation": "The derivative of x² is 2x using the power rule."},
                {"id": 2, "question": "What is 15 × 4?", "options": ["45", "55", "60", "65"], "correct_answer_index": 2, "explanation": "15 × 4 = 60"},
                {"id": 3, "question": "What is the square root of 144?", "options": ["10", "11", "12", "13"], "correct_answer_index": 2, "explanation": "12 × 12 = 144, so √144 = 12"},
            ],
            "python": [
                {"id": 1, "question": "What does len() return?", "options": ["First element", "Number of items", "Data type", "Memory address"], "correct_answer_index": 1, "explanation": "len() returns the number of items in a sequence."},
                {"id": 2, "question": "Which is a mutable data type?", "options": ["Tuple", "String", "List", "Integer"], "correct_answer_index": 2, "explanation": "Lists are mutable (can be modified), tuples and strings are immutable."},
                {"id": 3, "question": "How do you start a comment in Python?", "options": ["//", "/*", "#", "--"], "correct_answer_index": 2, "explanation": "Python comments start with the # symbol."},
            ],
            "biology": [
                {"id": 1, "question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"], "correct_answer_index": 1, "explanation": "Mitochondria produces energy (ATP) for the cell."},
                {"id": 2, "question": "How many pairs of chromosomes do humans have?", "options": ["20", "23", "46", "48"], "correct_answer_index": 1, "explanation": "Humans have 23 pairs of chromosomes (46 total)."},
                {"id": 3, "question": "What is the basic unit of life?", "options": ["Atom", "Molecule", "Cell", "Tissue"], "correct_answer_index": 2, "explanation": "The cell is the basic structural and functional unit of all living organisms."},
            ]
        }
        
        topic_lower = topic.lower()
        questions = demo_questions.get(topic_lower, demo_questions["math"])[:num_questions]
        
        # Pad with additional questions if needed
        while len(questions) < num_questions:
            questions.append({
                "id": len(questions) + 1,
                "question": f"What is an important concept in {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer_index": 0,
                "explanation": f"Review {topic} fundamentals."
            })
        
        return {"topic": topic, "difficulty": difficulty, "questions": questions[:num_questions]}

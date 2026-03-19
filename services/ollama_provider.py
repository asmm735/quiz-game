"""Ollama LLM Provider"""
import json
import requests
import hashlib
from typing import Dict, List, Any, Optional
from services.base_llm import BaseLLMProvider
from utils.prompts import *
from config.settings import OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT_EXPLAIN, OLLAMA_TIMEOUT_QUIZ, OLLAMA_TIMEOUT_EVALUATE, OLLAMA_RETRIES

class OllamaLLMProvider(BaseLLMProvider):
    """Ollama language model provider"""
    
    def __init__(self):
        super().__init__()
        self.model_name = OLLAMA_MODEL  # Use configured model (neural-chat)
        self.ollama_host = OLLAMA_HOST
        self.timeout_explain = OLLAMA_TIMEOUT_EXPLAIN
        self.timeout_quiz = OLLAMA_TIMEOUT_QUIZ
        self.timeout_evaluate = OLLAMA_TIMEOUT_EVALUATE
        self.retries = OLLAMA_RETRIES
        self._available = False
        self._detect_best_model()
        
    def _detect_best_model(self):
        """Detect best available model"""
        # Check if Ollama is available
        try:
            response = requests.get(f"{self.ollama_host}/api/tags", timeout=2)
            if response.status_code == 200:
                data = response.json()
                available_models = [m.get("name", "") for m in data.get("models", [])]
                
                # Prefer neural-chat if available
                if "neural-chat:latest" in available_models or "neural-chat" in str(available_models):
                    self.model_name = "neural-chat"
                    print("[OK] Ollama provider available with neural-chat")
                elif "orca-mini:latest" in available_models or "orca-mini" in str(available_models):
                    self.model_name = "orca-mini"
                    print("[OK] Ollama provider available with orca-mini")
                elif available_models:
                    self.model_name = available_models[0].split(":")[0]
                    print(f"[OK] Ollama provider available with {self.model_name}")
                else:
                    print("[WARN] Ollama has no models loaded")
                    self._available = False
                    return
                    
                self._available = True
            else:
                print("[WARN] Ollama not responding")
                self._available = False
        except Exception as e:
            print(f"[WARN] Ollama unavailable: {e}")
            self._available = False
    
    def is_available(self) -> bool:
        """Check if Ollama is available"""
        return self._available
    
    def _call_ollama(self, prompt: str, timeout: int = None, operation: str = "explain") -> str:
        """Call Ollama API with configurable timeout"""
        if timeout is None:
            if operation == "quiz":
                timeout = self.timeout_quiz
            elif operation == "evaluate":
                timeout = self.timeout_evaluate
            else:
                timeout = self.timeout_explain
        
        retries_left = self.retries
        last_error = None
        
        while retries_left >= 0:
            try:
                print(f"[INFO] Ollama call ({operation}) - Timeout: {timeout}s, Model: {self.model_name}")
                response = requests.post(
                    f"{self.ollama_host}/api/generate",
                    json={"model": self.model_name, "prompt": prompt, "stream": False},
                    timeout=timeout
                )
                if response.status_code == 200:
                    return response.json().get("response", "")
                raise Exception(f"HTTP {response.status_code}")
            except requests.exceptions.Timeout:
                last_error = f"Ollama timed out after {timeout} seconds"
                if retries_left > 0:
                    print(f"[RETRY] {last_error}, retries left: {retries_left}")
                    retries_left -= 1
                else:
                    raise Exception(last_error)
            except Exception as e:
                last_error = str(e)
                if retries_left > 0:
                    print(f"[RETRY] Ollama error: {e}, retries left: {retries_left}")
                    retries_left -= 1
                else:
                    raise
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """Extract JSON from LLM response"""
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
        """Generate cache key from function name and arguments"""
        key_str = f"{name}_{','.join(str(a) for a in args)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _validate_quiz(self, quiz_data: Dict) -> bool:
        """Validate that quiz questions are well-formed and real"""
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
                # Reject single-letter options (A, B, C, D)
                if len(opt_str) == 1 and opt_str in "ABCD":
                    print(f"[VALIDATE] Question {i+1} option {j} is single letter: {opt_str}")
                    return False
            
            # Check question is not a template
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
    
    def explain_concept(self, topic: str, question: str = None) -> Dict:
        """Explain a concept using Ollama"""
        if not self.is_available():
            return self._demo_explain(topic)
        
        # Check cache
        cache_key = self._get_cache_key("explain", topic)
        if cache_key in self.cache:
            print(f"[CACHE] Returning cached explanation for {topic}")
            return self.cache[cache_key]
        
        try:
            prompt = get_explain_concept_prompt(topic, question)
            print(f"[INFO] Explaining: {topic}")
            response_text = self._call_ollama(prompt, operation="explain")
            result = self._extract_json(response_text)
            if result and "simple_explanation" in result:
                self.cache[cache_key] = result
                print(f"[OK] Explanation received")
                return result
            return self._demo_explain(topic)
        except Exception as e:
            print(f"[FAIL] Explanation failed: {e}")
            return self._demo_explain(topic)
    
    def generate_quiz_questions(self, topic: str, difficulty: str, num_questions: int) -> Dict:
        """Generate quiz questions using Ollama"""
        if not self.is_available():
            return self._demo_quiz(topic, difficulty, num_questions)
        
        # Check cache
        cache_key = self._get_cache_key("quiz", topic, difficulty, num_questions)
        if cache_key in self.cache:
            print(f"[CACHE] Returning cached quiz for {topic} ({difficulty})")
            return self.cache[cache_key]
        
        try:
            prompt = get_quiz_generation_prompt(topic, difficulty, num_questions)
            print(f"[INFO] Generating quiz for: {topic} ({difficulty})")
            response_text = self._call_ollama(prompt, operation="quiz")
            
            result = self._extract_json(response_text)
            if result and self._validate_quiz(result):
                questions = result.get("questions", [])
                if len(questions) > 0:
                    self.cache[cache_key] = result
                    print(f"[OK] Generated {len(questions)} questions")
                    return result
            
            print(f"[WARN] Validation failed, using fallback")
            return self._demo_quiz(topic, difficulty, num_questions)
        except Exception as e:
            print(f"[FAIL] Quiz generation: {e}")
            return self._demo_quiz(topic, difficulty, num_questions)
    
    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, options: List[str]) -> Dict:
        """Evaluate answer using Ollama"""
        if not self.is_available():
            is_correct = user_answer.lower() == correct_answer.lower()
            return {"is_correct": is_correct, "score": 100 if is_correct else 30, "explanation": "Good", "improvement_tip": "Practice", "similar_concept": "Related"}
        try:
            prompt = get_evaluate_answer_prompt(question, user_answer, correct_answer, options)
            response_text = self._call_ollama(prompt, operation="evaluate")
            result = self._extract_json(response_text)
            if result and "is_correct" in result:
                return result
            return {"is_correct": False, "score": 0, "explanation": "Error", "improvement_tip": "Review", "similar_concept": "N/A"}
        except Exception as e:
            return {"is_correct": False, "score": 0, "explanation": "Error", "improvement_tip": "Review", "similar_concept": "N/A"}
    
    def explain_wrong_answer(self, question: str, user_answer: str, correct_answer: str, explanation: str) -> Dict:
        """Explain wrong answer using Ollama"""
        if not self.is_available():
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
        try:
            prompt = get_explain_wrong_answer_prompt(question, user_answer, correct_answer, explanation)
            response_text = self._call_ollama(prompt, operation="evaluate")
            result = self._extract_json(response_text)
            if result and "misconception" in result:
                return result
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
        except Exception as e:
            return {"misconception": "Review", "correct_thinking": "Focus", "mnemonic_or_trick": "Remember", "next_steps": "Practice"}
    
    def _demo_explain(self, topic: str) -> Dict:
        """Demo explanation"""
        return {"simple_explanation": f"{topic} is fundamental.", "real_world_analogy": f"Like learning {topic}.", "key_points": ["P1", "P2", "P3"], "follow_up_question": f"What is {topic}?", "fun_fact": f"Fun: {topic}!"}
    
    def _demo_quiz(self, topic: str, difficulty: str, num_questions: int) -> Dict:
        """Demo quiz questions - topic-specific fallback"""
        demo_questions = {
            "recursion": [
                {"id": 1, "question": "What is the base case in a recursive function?", "options": ["The function that calls itself", "The condition that stops the recursion", "The first parameter passed", "The return type of the function"], "correct_answer_index": 1, "explanation": "The base case is the condition that stops the recursive function from calling itself infinitely, preventing a stack overflow."},
                {"id": 2, "question": "Which of these is a problem suitable for recursion?", "options": ["Printing numbers 1 to 10 in order", "Calculating factorial of a number", "Reading a file line by line", "Updating a single database record"], "correct_answer_index": 1, "explanation": "Calculating factorial is ideal for recursion as each step divides the problem: n! = n × (n-1)!"},
                {"id": 3, "question": "What happens if a recursive function has no base case?", "options": ["It runs faster", "It causes a stack overflow error", "It returns None", "It runs indefinitely without error"], "correct_answer_index": 1, "explanation": "Without a base case, the function calls itself indefinitely, consuming memory until the call stack overflows and crashes the program."},
                {"id": 4, "question": "In the Fibonacci sequence using recursion, which problem occurs?", "options": ["The function never terminates", "Many calculations are repeated unnecessarily", "The function needs a class", "Recursion cannot work for Fibonacci"], "correct_answer_index": 1, "explanation": "Naive recursive Fibonacci recalculates the same values many times. For example, fib(5) calculates fib(3) multiple times, causing exponential time complexity."},
                {"id": 5, "question": "What is the main difference between recursion and iteration?", "options": ["Recursion uses memory, iteration doesn't", "Recursion uses a call stack, iteration uses loops", "Iteration is always faster", "Recursion can solve problems iteration cannot"], "correct_answer_index": 1, "explanation": "Recursion uses the call stack to store function calls, while iteration uses loops. Both can solve similar problems, but recursion uses more memory."},
            ],
            "python": [
                {"id": 1, "question": "What does len() return?", "options": ["First element", "Number of items", "Data type", "Memory address"], "correct_answer_index": 1, "explanation": "len() returns the number of items in a sequence."},
                {"id": 2, "question": "Which is a mutable data type?", "options": ["Tuple", "String", "List", "Integer"], "correct_answer_index": 2, "explanation": "Lists are mutable (can be modified), tuples and strings are immutable."},
                {"id": 3, "question": "How do you start a comment in Python?", "options": ["//", "/*", "#", "--"], "correct_answer_index": 2, "explanation": "Python comments start with the # symbol."},
            ],
            "math": [
                {"id": 1, "question": "What is the derivative of x²?", "options": ["x", "2x", "x²", "2"], "correct_answer_index": 1, "explanation": "The derivative of x² is 2x using the power rule."},
                {"id": 2, "question": "What is 15 × 4?", "options": ["45", "55", "60", "65"], "correct_answer_index": 2, "explanation": "15 × 4 = 60"},
                {"id": 3, "question": "What is the square root of 144?", "options": ["10", "11", "12", "13"], "correct_answer_index": 2, "explanation": "12 × 12 = 144, so √144 = 12"},
            ],
            "biology": [
                {"id": 1, "question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Golgi apparatus"], "correct_answer_index": 1, "explanation": "Mitochondria produces energy (ATP) for the cell."},
                {"id": 2, "question": "How many pairs of chromosomes do humans have?", "options": ["20", "23", "46", "48"], "correct_answer_index": 1, "explanation": "Humans have 23 pairs of chromosomes (46 total)."},
                {"id": 3, "question": "What is the basic unit of life?", "options": ["Atom", "Molecule", "Cell", "Tissue"], "correct_answer_index": 2, "explanation": "The cell is the basic structural and functional unit of all living organisms."},
            ],
            "data structures": [
                {"id": 1, "question": "What is the time complexity of accessing an element in an array?", "options": ["O(n)", "O(log n)", "O(1)", "O(n²)"], "correct_answer_index": 2, "explanation": "Array access is O(1) because you can directly access any element using its index."},
                {"id": 2, "question": "Which data structure uses LIFO (Last In First Out)?", "options": ["Queue", "Stack", "Heap", "Tree"], "correct_answer_index": 1, "explanation": "A stack uses LIFO - the last item pushed is the first one popped out."},
                {"id": 3, "question": "What is a linked list useful for?", "options": ["Fast random access", "Efficient insertion/deletion", "Storing sorted data", "Fixed-size collections"], "correct_answer_index": 1, "explanation": "Linked lists excel at insertion and deletion operations as they don't require shifting elements."},
            ],
            "algorithms": [
                {"id": 1, "question": "What is the best-case time complexity of bubble sort?", "options": ["O(n log n)", "O(n)", "O(n²)", "O(1)"], "correct_answer_index": 1, "explanation": "Bubble sort has O(n) best case when the array is already sorted (only one pass needed)."},
                {"id": 2, "question": "Which sorting algorithm is most suitable for nearly sorted data?", "options": ["Merge sort", "Quick sort", "Insertion sort", "Selection sort"], "correct_answer_index": 2, "explanation": "Insertion sort performs best on nearly sorted data, with O(n) complexity in the best case."},
                {"id": 3, "question": "What does Big O notation measure?", "options": ["Memory usage only", "Time complexity only", "Time and space complexity as input grows", "Number of lines of code"], "correct_answer_index": 2, "explanation": "Big O describes how an algorithm's performance scales as the input size increases."},
            ]
        }
        
        topic_lower = topic.lower()
        questions = demo_questions.get(topic_lower, demo_questions["python"])[:num_questions]
        
        while len(questions) < num_questions:
            questions.append({
                "id": len(questions) + 1,
                "question": f"What is an important concept in {topic}?",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer_index": 0,
                "explanation": f"Review {topic} fundamentals."
            })
        
        return {"topic": topic, "difficulty": difficulty, "questions": questions[:num_questions]}

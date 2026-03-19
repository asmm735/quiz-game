"""Base LLM Provider Interface"""
from abc import ABC, abstractmethod
from typing import Dict, List, Optional


class BaseLLMProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(self):
        """Initialize LLM provider with caching"""
        self.cache = {}
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is available"""
        pass
    
    @abstractmethod
    def explain_concept(self, topic: str, question: str = None) -> Dict:
        """Explain a concept"""
        pass
    
    @abstractmethod
    def generate_quiz_questions(self, topic: str, difficulty: str, num_questions: int) -> Dict:
        """Generate quiz questions"""
        pass
    
    @abstractmethod
    def evaluate_answer(self, question: str, user_answer: str, correct_answer: str, options: List[str]) -> Dict:
        """Evaluate user's answer"""
        pass
    
    @abstractmethod
    def explain_wrong_answer(self, question: str, user_answer: str, correct_answer: str, explanation: str) -> Dict:
        """Explain why answer is wrong"""
        pass

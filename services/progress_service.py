import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class ProgressStore:
    """Handles saving and loading student progress"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.progress_file = self.data_dir / "student_progress.json"
        self.quiz_history_file = self.data_dir / "quiz_history.json"
    
    def load_progress(self) -> Dict[str, Any]:
        """Load existing progress or create new"""
        if self.progress_file.exists():
            try:
                with open(self.progress_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._create_default_progress()
        return self._create_default_progress()
    
    def save_progress(self, progress: Dict[str, Any]) -> None:
        """Save progress to file"""
        try:
            with open(self.progress_file, 'w') as f:
                json.dump(progress, f, indent=2)
        except IOError as e:
            print(f"Error saving progress: {e}")
    
    def load_quiz_history(self) -> List[Dict[str, Any]]:
        """Load quiz attempt history"""
        if self.quiz_history_file.exists():
            try:
                with open(self.quiz_history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_quiz_attempt(self, attempt: Dict[str, Any]) -> None:
        """Add a quiz attempt to history"""
        history = self.load_quiz_history()
        attempt['timestamp'] = datetime.now().isoformat()
        history.append(attempt)
        
        try:
            with open(self.quiz_history_file, 'w') as f:
                json.dump(history, f, indent=2)
        except IOError as e:
            print(f"Error saving quiz attempt: {e}")
    
    def _create_default_progress(self) -> Dict[str, Any]:
        """Create default progress structure"""
        return {
            'name': 'Student',
            'grade': 'NA',
            'subject': 'General',
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'gamification': {
                'points': 0,
                'streak': 0,
                'best_streak': 0,
                'topics_explored': [],
                'badges_earned': [],
                'level': 1
            },
            'quizzes': {
                'attempted': 0,
                'accuracy_percentage': 0,
                'recent_topics': []
            }
        }
    
    def update_progress(self, 
                       name: str = None,
                       grade: str = None,
                       subject: str = None,
                       gamification: Dict = None,
                       quiz_stats: Dict = None) -> None:
        """Update various parts of progress"""
        progress = self.load_progress()
        
        if name:
            progress['name'] = name
        if grade:
            progress['grade'] = grade
        if subject:
            progress['subject'] = subject
        if gamification:
            progress['gamification'] = gamification
        if quiz_stats:
            progress['quizzes'] = quiz_stats
        
        progress['last_updated'] = datetime.now().isoformat()
        self.save_progress(progress)
    
    def get_stats_summary(self) -> Dict[str, Any]:
        """Get summary statistics"""
        progress = self.load_progress()
        history = self.load_quiz_history()
        
        # Calculate accuracy
        correct = sum(1 for q in history if q.get('score', 0) >= 70)
        total = len(history)
        accuracy = (correct / total * 100) if total > 0 else 0
        
        # Get recent topics
        recent_topics = list(set(q.get('topic', 'Unknown') for q in history[-10:]))
        
        return {
            'name': progress.get('name', 'Student'),
            'grade': progress.get('grade', 'NA'),
            'subject': progress.get('subject', 'General'),
            'total_points': progress['gamification']['points'],
            'current_level': progress['gamification']['level'],
            'quizzes_attempted': len(history),
            'accuracy_percentage': round(accuracy, 1),
            'badges_earned': progress['gamification']['badges_earned'],
            'recent_topics': recent_topics,
            'current_streak': progress['gamification']['streak'],
            'best_streak': progress['gamification']['best_streak'],
            'topics_explored': len(progress['gamification']['topics_explored'])
        }

"""User Authentication and Management Service"""
import json
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

class UserService:
    """Manages user authentication, registration, and profile data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.users_file = self.data_dir / "users.json"
        self.current_user = None
        self._load_users()
    
    def _load_users(self):
        """Load users from file"""
        if self.users_file.exists():
            try:
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.users = {}
        else:
            self.users = {}
    
    def _save_users(self):
        """Save users to file"""
        try:
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=2)
        except IOError as e:
            print(f"Error saving users: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def register(self, username: str, password: str) -> tuple[bool, str]:
        """Register a new user"""
        if not username or not password:
            return False, "Username and password are required"
        
        if username in self.users:
            return False, f"User '{username}' already exists"
        
        self.users[username] = {
            "password": self._hash_password(password),
            "created_at": datetime.now().isoformat(),
            "stats": {
                "points": 0,
                "level": 1,
                "streak": 0,
                "badges": [],
                "quizzes_attempted": 0,
                "accuracy": 0.0
            },
            "quiz_history": []
        }
        self._save_users()
        return True, f"User '{username}' registered successfully!"
    
    def login(self, username: str, password: str) -> tuple[bool, str]:
        """Authenticate user"""
        if username not in self.users:
            return False, f"User '{username}' not found"
        
        if self.users[username]["password"] != self._hash_password(password):
            return False, "Incorrect password"
        
        self.current_user = username
        return True, f"Welcome back, {username}!"
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
    
    def get_current_user(self) -> Optional[str]:
        """Get currently logged-in user"""
        return self.current_user
    
    def get_user_stats(self, username: str = None) -> Optional[Dict[str, Any]]:
        """Get user's statistics"""
        user = username or self.current_user
        if not user or user not in self.users:
            return None
        return self.users[user]["stats"]
    
    def add_quiz_attempt(self, topic: str, difficulty: str, score: float, correct: int, total: int) -> None:
        """Record a quiz attempt and update stats"""
        if not self.current_user:
            return
        
        user_data = self.users[self.current_user]
        stats = user_data["stats"]
        
        # Calculate points earned
        points_earned = int(score * 10)  # 0-100 score = 0-1000 points
        if correct == total:
            points_earned = int(points_earned * 1.5)  # 50% bonus for perfect
        
        # Update stats
        stats["points"] += points_earned
        stats["quizzes_attempted"] += 1
        
        # Update accuracy
        if stats["quizzes_attempted"] > 0:
            stats["accuracy"] = (stats.get("total_correct", 0) + correct) / (stats["quizzes_attempted"] * total) * 100
            stats["total_correct"] = stats.get("total_correct", 0) + correct
        
        # Update streak
        if score >= 80:
            stats["streak"] = stats.get("current_streak", 0) + 1
        else:
            stats["current_streak"] = 0
        
        # Level up logic
        if stats["points"] >= 1000 and stats["level"] == 1:
            stats["level"] = 2
            stats["badges"].append("Bronze Learner")
        elif stats["points"] >= 5000 and stats["level"] == 2:
            stats["level"] = 3
            stats["badges"].append("Silver Expert")
        elif stats["points"] >= 10000 and stats["level"] == 3:
            stats["level"] = 4
            stats["badges"].append("Gold Master")
        
        # Track quiz history
        user_data["quiz_history"].append({
            "topic": topic,
            "difficulty": difficulty,
            "score": score,
            "correct": correct,
            "total": total,
            "points_earned": points_earned,
            "timestamp": datetime.now().isoformat()
        })
        
        self._save_users()
    
    def get_all_users_stats(self) -> Dict[str, Dict]:
        """Get leaderboard data"""
        leaderboard = {}
        for username, data in self.users.items():
            leaderboard[username] = {
                "points": data["stats"]["points"],
                "level": data["stats"]["level"],
                "accuracy": data["stats"]["accuracy"],
                "badges": len(data["stats"]["badges"])
            }
        # Sort by points
        return dict(sorted(leaderboard.items(), key=lambda x: x[1]["points"], reverse=True))

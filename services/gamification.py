from typing import Dict, List, Tuple

class GamificationEngine:
    """Handles points, levels, streaks, and badges"""
    
    # Configuration
    POINTS_PER_CORRECT = 10
    STREAK_BONUS = 5
    STREAK_THRESHOLD = 3  # bonus after 3 correct in a row
    
    # Level thresholds
    LEVEL_THRESHOLDS = {
        1: (0, 49),
        2: (50, 99),
        3: (100, 199),
        4: (200, 399),
        5: (400, float('inf'))
    }
    
    # Badge definitions
    BADGES = {
        "Quiz Starter": {"threshold": 50, "description": "Answered 5 questions correctly"},
        "Concept Explorer": {"threshold": 100, "description": "Explored 10 different topics"},
        "Concept Master": {"threshold": 200, "description": "Scored 200+ total points"},
        "Streak Champ": {"threshold": 10, "description": "Achieved 10 correct in a row"},
        "Perfect Streak": {"threshold": 5, "description": "5 Perfect scores in a row"},
        "Quiz Champion": {"threshold": 500, "description": "Reached 500 total points"},
    }
    
    def __init__(self):
        self.points = 0
        self.streak = 0
        self.topics_explored = set()
        self.badges_earned = []
        self.level = 1
        self.best_streak = 0
    
    def load_from_dict(self, data: Dict):
        """Load gamification state from dictionary"""
        self.points = data.get('points', 0)
        self.streak = data.get('streak', 0)
        self.best_streak = data.get('best_streak', 0)
        self.topics_explored = set(data.get('topics_explored', []))
        self.badges_earned = data.get('badges_earned', [])
        self.level = self.calculate_level(self.points)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'points': self.points,
            'streak': self.streak,
            'best_streak': self.best_streak,
            'topics_explored': list(self.topics_explored),
            'badges_earned': self.badges_earned,
            'level': self.level
        }
    
    def add_correct_answer(self, topic: str) -> Tuple[int, int, List[str]]:
        """
        Called when student answers correctly.
        Returns: (points_awarded, streak_bonus, new_badges)
        """
        points_awarded = self.POINTS_PER_CORRECT
        streak_bonus = 0
        new_badges = []
        
        # Update streak
        self.streak += 1
        if self.streak > self.best_streak:
            self.best_streak = self.streak
        
        # Streak bonus every N correct
        if self.streak % self.STREAK_THRESHOLD == 0:
            streak_bonus = self.STREAK_BONUS
        
        self.points += points_awarded + streak_bonus
        self.topics_explored.add(topic)
        
        # Check for new badges
        new_badges = self._check_badges()
        self.level = self.calculate_level(self.points)
        
        return points_awarded, streak_bonus, new_badges
    
    def add_wrong_answer(self) -> None:
        """Called when student answers incorrectly"""
        self.streak = 0
    
    def calculate_level(self, points: int) -> int:
        """Determine level based on points"""
        for level, (min_pts, max_pts) in self.LEVEL_THRESHOLDS.items():
            if min_pts <= points <= max_pts:
                return level
        return 1
    
    def get_level_progress(self) -> Dict:
        """Get progress within current level"""
        min_pts, max_pts = self.LEVEL_THRESHOLDS[self.level]
        
        if max_pts == float('inf'):
            # Last level - just show points
            return {
                'current_level': self.level,
                'current_points': self.points,
                'level_min': min_pts,
                'level_max': None,
                'progress_percentage': 100
            }
        
        progress = ((self.points - min_pts) / (max_pts - min_pts + 1)) * 100
        progress = min(progress, 100)
        
        return {
            'current_level': self.level,
            'current_points': self.points,
            'level_min': min_pts,
            'level_max': max_pts,
            'progress_percentage': progress
        }
    
    def _check_badges(self) -> List[str]:
        """Check if any badges were newly earned"""
        newly_earned = []
        
        # Check each badge condition
        if self.points >= self.BADGES["Quiz Starter"]["threshold"] and "Quiz Starter" not in self.badges_earned:
            newly_earned.append("Quiz Starter")
            self.badges_earned.append("Quiz Starter")
        
        if len(self.topics_explored) >= 10 and "Concept Explorer" not in self.badges_earned:
            newly_earned.append("Concept Explorer")
            self.badges_earned.append("Concept Explorer")
        
        if self.points >= self.BADGES["Concept Master"]["threshold"] and "Concept Master" not in self.badges_earned:
            newly_earned.append("Concept Master")
            self.badges_earned.append("Concept Master")
        
        if self.best_streak >= self.BADGES["Streak Champ"]["threshold"] and "Streak Champ" not in self.badges_earned:
            newly_earned.append("Streak Champ")
            self.badges_earned.append("Streak Champ")
        
        if self.points >= self.BADGES["Quiz Champion"]["threshold"] and "Quiz Champion" not in self.badges_earned:
            newly_earned.append("Quiz Champion")
            self.badges_earned.append("Quiz Champion")
        
        return newly_earned
    
    def get_stats(self) -> Dict:
        """Get complete gamification stats"""
        return {
            'total_points': self.points,
            'current_level': self.level,
            'current_streak': self.streak,
            'best_streak': self.best_streak,
            'topics_explored': len(self.topics_explored),
            'badges_earned': len(self.badges_earned),
            'badges_list': self.badges_earned,
            'level_progress': self.get_level_progress()
        }

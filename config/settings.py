"""
Application Configuration and Settings
"""

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "AI Quiz Tutor",
    "page_icon": "🎓",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# LLM Configuration
OLLAMA_HOST = "http://localhost:11434"
OLLAMA_MODEL = "neural-chat"  # Fast model (10-30s per request)
OLLAMA_TIMEOUT_EXPLAIN = 120   # seconds for explanations
OLLAMA_TIMEOUT_QUIZ = 600      # seconds for quiz generation (generous timeout for resource-heavy ops)
OLLAMA_TIMEOUT_EVALUATE = 120  # seconds for answer evaluation
OLLAMA_RETRIES = 1             # Reduce retries to avoid long waits

# Gamification System
GAMIFICATION = {
    "points_per_answer": 10,
    "streak_bonus_frequency": 3,  # Every 3 correct answers
    "streak_bonus_points": 5,
}

# Level Thresholds (points required)
LEVEL_THRESHOLDS = {
    1: 0,
    2: 50,
    3: 100,
    4: 200,
    5: 400,
}

# Badge Requirements
BADGES = {
    "Quiz Starter": {"type": "points", "value": 50},
    "Concept Explorer": {"type": "topics", "value": 10},
    "Concept Master": {"type": "points", "value": 200},
    "Streak Champ": {"type": "streak", "value": 10},
    "Quiz Champion": {"type": "points", "value": 500},
}

# Data Storage
DATA_DIR = "data"
USERS_FILE = f"{DATA_DIR}/users.json"
CACHE_HASH_ALGORITHM = "md5"

# Quiz Generation
QUIZ_DIFFICULTIES = ["Easy", "Medium", "Hard"]
MAX_QUESTIONS_PER_QUIZ = 10
MIN_QUESTIONS_PER_QUIZ = 1

# Response Validation
MIN_RESPONSE_LENGTH = 10
PLACEHOLDER_KEYWORDS = ["fundamental", "basic", "simple"]

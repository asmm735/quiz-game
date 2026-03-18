# ⚙️ Configuration Guide

## 🔑 Environment Variables

### Required
```bash
# .env file
OPENAI_API_KEY=sk_xxxxxxxxxxxxxxxxxxxx
```

### Optional (for future use)
```bash
# LLM Configuration
LLM_MODEL=gpt-3.5-turbo
LLM_TEMPERATURE=0.7

# Storage
DATA_DIR=data
```

---

## 🎮 Gamification Configuration

Edit `services/gamification.py` to customize:

### Points System
```python
class GamificationEngine:
    POINTS_PER_CORRECT = 10      # Change this
    STREAK_BONUS = 5             # Change this
    STREAK_THRESHOLD = 3         # Bonus every N correct
```

**Example: Award more points**
```python
POINTS_PER_CORRECT = 15    # Instead of 10
STREAK_BONUS = 10          # Instead of 5
```

### Level Thresholds
```python
LEVEL_THRESHOLDS = {
    1: (0, 49),              # Level 1: 0-49 points
    2: (50, 99),             # Level 2: 50-99 points
    3: (100, 199),           # Level 3: 100-199 points
    4: (200, 399),           # Level 4: 200-399 points
    5: (400, float('inf'))   # Level 5: 400+ points
}
```

**Example: More levels**
```python
LEVEL_THRESHOLDS = {
    1: (0, 24),
    2: (25, 49),
    3: (50, 99),
    4: (100, 199),
    5: (200, 399),
    6: (400, 799),
    7: (800, float('inf'))
}
```

### Badge Configuration
```python
BADGES = {
    "Quiz Starter": {
        "threshold": 50,
        "description": "Answered 5 questions correctly"
    },
    # Add more badges here
}
```

**Example: Add a new badge**
```python
"Power Learner": {
    "threshold": 1000,
    "description": "Reached 1000 total points!"
},
```

Then add unlock logic in `_check_badges()`:
```python
if self.points >= self.BADGES["Power Learner"]["threshold"] \
   and "Power Learner" not in self.badges_earned:
    newly_earned.append("Power Learner")
    self.badges_earned.append("Power Learner")
```

---

## 🤖 LLM Configuration

Edit `services/llm_service.py` to customize:

### Model Selection
```python
class LLMService:
    def __init__(self):
        self.model = "gpt-3.5-turbo"  # Change this
```

**Available models:**
```python
"gpt-3.5-turbo"     # Fast, cheap (recommended)
"gpt-4"             # Smarter, slower, expensive
"gpt-4-turbo"       # Better balance
```

### Temperature Settings
```python
response = self.client.chat.completions.create(
    model=self.model,
    messages=[...],
    temperature=0.7,  # Change this
)
```

**Temperature guide:**
- `0.0`: Deterministic (same answer every time)
- `0.3-0.5`: Focused, consistent
- `0.5-0.7`: Balanced (default)
- `0.8-1.0`: Creative, varied
- `1.0+`: Very random

**Recommended values:**
```python
# Explanations: More creative
explain_response = client.create(..., temperature=0.8)

# Quiz generation: More consistent
quiz_response = client.create(..., temperature=0.6)

# Evaluation: Strict
eval_response = client.create(..., temperature=0.3)
```

### Prompt Engineering

#### Change explanation style
In `explain_concept()`, modify the prompt:

**Current (simple language):**
```python
prompt = f"""You are a friendly physics/math/programming tutor.
Explain [TOPIC] in very simple language."""
```

**Change to (technical):**
```python
prompt = f"""You are a technical expert.
Provide a detailed technical explanation of [TOPIC]."""
```

#### Change quiz difficulty descriptions
In `generate_quiz_questions()`:

```python
difficulty_desc = {
    "easy": "very basic concept understanding, simple vocabulary",
    "medium": "intermediate understanding, practical application",
    "hard": "deep understanding, edge cases, critical thinking"
}

# Customize:
difficulty_desc = {
    "easy": "basic, think 5th grader",
    "medium": "high school level",
    "hard": "college course level"
}
```

### Output Format Customization

Change JSON structure for explanations:

```python
# Current structure
return {
    "simple_explanation": "...",
    "real_world_analogy": "...",
    "key_points": [],
    "follow_up_question": "...",
    "fun_fact": "..."
}

# Add more fields:
return {
    "simple_explanation": "...",
    "real_world_analogy": "...",
    "key_points": [],
    "follow_up_question": "...",
    "fun_fact": "...",
    "historical_context": "...",     # NEW
    "common_mistakes": [],           # NEW
    "next_topic_suggestion": "..."   # NEW
}
```

---

## 💾 Storage Configuration

Edit `services/progress_service.py`:

### Change data directory
```python
class ProgressStore:
    def __init__(self, data_dir: str = "data"):  # Change this
        self.data_dir = Path(data_dir)
```

**Examples:**
```python
ProgressStore("data")           # Current folder/data
ProgressStore("/home/user/quiz_data")
ProgressStore("C:\\quiz_data\\")
```

### Add custom fields to progress
```python
def _create_default_progress(self):
    return {
        'name': 'Student',
        'grade': 'NA',
        'subject': 'General',
        
        # Add custom fields:
        'school': 'My School',
        'teacher': 'Mr. Smith',
        'last_login': datetime.now().isoformat(),
        
        # ... rest of structure
    }
```

### Enable multi-user support (advanced)

```python
def __init__(self, user_id: str, data_dir: str = "data"):
    self.user_id = user_id
    self.data_dir = Path(data_dir) / user_id
    self.data_dir.mkdir(exist_ok=True)
    # ... rest of init

# Usage:
store = ProgressStore("student_123")
```

---

## 🎨 UI Customization

Edit `app.py` to customize:

### Change app title
```python
st.set_page_config(
    page_title="AI Quiz Tutor",  # Change this
    page_icon="🎓",              # Change this
    layout="wide",
)
```

### Change sidebar title
```python
st.markdown("## 📚 Navigation")  # Change text
st.markdown("## 📊 Quick Stats")  # Change text
```

### Add new sections
```python
page = st.radio(
    "Choose a section:",
    ["Home", "Ask the Tutor", "Generate Quiz", "My New Section", "Progress Dashboard"],
    key="page_selector"
)

# Add handler
if page == "My New Section":
    show_my_new_section()

def show_my_new_section():
    st.markdown("## 🆕 My New Section")
    # Your content here
```

### Change colors and styling
```python
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .badge {
        background: #FFD700;
        color: #333;
    }
</style>
""", unsafe_allow_html=True)

# Change gradient colors:
# #667eea → #764ba2 (purple)
# Change to your colors
```

---

## 📱 Streamlit Configuration

Create `~/.streamlit/config.toml` for global settings:

```toml
[theme]
primaryColor = "#667eea"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#262730"
textColor = "#fafafa"

[client]
showErrorDetails = true
```

Or create `.streamlit/config.toml` in project root:

```toml
[logger]
level = "info"

[server]
port = 8501
headless = true
```

---

## 🚀 Performance Optimization

### Caching API responses
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_quiz(topic, difficulty):
    return llm_service.generate_quiz_questions(topic, difficulty, 5)
```

### Reduce API calls
```python
# Bad: Calls API every click
if st.button("Explain"):
    explanation = llm_service.explain_concept(topic)

# Better: Cache results
if 'explanation' not in st.session_state:
    st.session_state.explanation = llm_service.explain_concept(topic)
```

### Optimize data loading
```python
# Current: Load full history every time
history = st.session_state.progress_store.load_quiz_history()

# Better: Cache and update only when needed
@st.cache_data
def get_quiz_history():
    return st.session_state.progress_store.load_quiz_history()

history = get_quiz_history()
```

---

## 🔒 Security Configuration

### Protect API keys
```python
# Current: Uses .env file
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Better for production: Use Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]
```

For Streamlit Cloud, add to `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk_..."
```

### Add rate limiting
```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_calls: int, time_window: int):
        self.max_calls = max_calls
        self.time_window = time_window
        self.calls = []
    
    def is_allowed(self) -> bool:
        now = datetime.now()
        self.calls = [c for c in self.calls 
                     if c > now - timedelta(seconds=self.time_window)]
        
        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False
```

---

## 📊 Analytics Configuration (Advanced)

Track usage patterns:

```python
def log_event(event_type: str, data: dict):
    """Log events for analytics"""
    event = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'data': data
    }
    
    with open('events.jsonl', 'a') as f:
        f.write(json.dumps(event) + '\n')

# Usage:
log_event('quiz_completed', {
    'topic': 'Recursion',
    'score': 80,
    'difficulty': 'medium'
})
```

---

## 🔄 Deployment Configuration

### For Streamlit Cloud
1. Create `.streamlit/secrets.toml`:
```toml
OPENAI_API_KEY = "sk_..."
```

2. Push to GitHub and deploy from Streamlit Cloud

### For Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py"]
```

### For Hugging Face Spaces
1. Create `requirements.txt`
2. Create `app.py`
3. Create `.env` with API key
4. Push to Hugging Face

---

## ✅ Configuration Checklist

- [ ] API key set in `.env`
- [ ] Gamification points configured
- [ ] Badge thresholds set
- [ ] Prompts customized to your use case
- [ ] Data directory configured
- [ ] UI customized with your branding
- [ ] Rate limiting enabled (optional)
- [ ] Analytics logging enabled (optional)
- [ ] Tested all features after configuration

---

Need help? Check [README.md](README.md) or [ARCHITECTURE.md](ARCHITECTURE.md)

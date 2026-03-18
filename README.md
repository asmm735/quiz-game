# 🎓 AI Quiz Tutor - Interactive Learning Platform

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-412991?logo=github&logoColor=white)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

A production-grade educational platform combining AI explanations, quiz generation, gamification, and progress tracking — completely offline using Ollama.

---

## 🌟 What Makes This Special

This project demonstrates complete full-stack development with:
- ✅ AI-Powered Explanations (via Ollama locally, Gemini as fallback)
- ✅ Intelligent Quiz Generation (multiple difficulty levels)
- ✅ Advanced Gamification (points, levels, badges, streaks)
- ✅ Real-Time Progress Tracking (per-user analytics)
- ✅ Zero Cost Operation (Ollama is completely local & free)
- ✅ Service-Oriented Architecture (modular, maintainable code)
- ✅ Production-Ready Error Handling (validation, retries, fallbacks)

---

## ✨ Core Features

### 💡 Ask the Tutor
Get AI-powered explanations with:
- Real-world analogies and practical examples
- Key learning points summary
- Follow-up questions to verify understanding
- Interesting facts and context
- Response time: 10-30 seconds (local neural-chat model)

### 📝 Generate Quiz
AI-generated quizzes with:
- Multiple difficulty levels (Easy, Medium, Hard)
- AI-generated multiple choice questions
- Detailed explanations for all answers
- "Explain Wrong Answer" feature for deeper learning
- Smart scoring: 10 points per correct answer + 5 bonus per 3-answer streak
- Response time: 20-120 seconds depending on question count

### 🎮 Gamification Engine

Complete point system with:
```
Points:       10 per correct answer + 5 per 3-correct streak
Levels:       1-5 progression (0 → 400+ points)
Badges:       5 collectible milestones
Streaks:      Current + personal best tracking
Accuracy:     Real-time performance metrics
```

### 📊 Progress Dashboard
Track every metric that matters:
- Total points and level progression
- Quiz history with scores and dates
- Accuracy percentage per topic
- Current and best streak visualization
- Badge achievements display

### 🏆 Global Leaderboard
Competitive ranking system showing:
- User rankings by points
- Performance comparisons
- Real-time updates

---

## 🚀 Quick Start (5 Minutes)

### Prerequisites
- Python 3.8+
- Ollama (free, local LLM runtime from https://ollama.ai)
- Optional: Google API key for Gemini as fallback

### Installation

```bash
# Clone repository
git clone https://github.com/YOUR_USERNAME/quiz-game.git
cd quiz-game

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Setup Ollama

```bash
# Download from https://ollama.ai and install

# Pull the neural-chat model (fast - 10-30s responses)
ollama pull neural-chat

# Verify it works
curl http://localhost:11434/api/tags
```

### Run the App

```bash
streamlit run app.py
```

Open browser: **http://localhost:8501** 🎉

---

## 🛠️ Technical Architecture

### LLM Provider System

```
Primary:   Ollama (neural-chat model)
  → Completely local & free
  → Works offline
  → 10-30 seconds per response

Fallback:  Google Gemini
  → Used if Ollama unavailable
  → Requires GOOGLE_API_KEY in .env
  → Cloud-based but fast
```

### Current Status
- **Active LLM**: Ollama (neural-chat) ✅
- **Fallback Available**: Gemini (requires API key)
- **Why Ollama Primary**: Completely free, offline operation, no API quota limits

### Architecture Components

| Service | Purpose | Tech |
|---------|---------|------|
| **LLMService** | AI routing, response caching, timeout management | Ollama + Gemini |
| **UserService** | User auth, per-user tracking | SHA-256, JSON |
| **GamificationEngine** | Points, levels, badges, streaks | Custom logic |
| **ProgressStore** | Data persistence, quiz history | JSON files |

### Smart Features

- ✅ Dual-provider LLM router (Ollama → Gemini → error)
- ✅ Auto-model detection (neural-chat → orca-mini → available)
- ✅ Response caching (MD5-based, prevents regeneration)
- ✅ Intelligent timeouts (45s explain, 120s quiz, 60s eval)
- ✅ Retry mechanism (2 retries on timeout)
- ✅ Validation layers (quality checks, placeholder rejection)

### Performance Metrics

| Scenario | Time |
|----------|------|
| Cold start (model init) | ~45 seconds |
| Warm explanations | 10-30 seconds |
| Quiz generation (5 Qs) | 20-120 seconds |
| Cached responses | <1 second |

---

## 📁 Project Structure

```
quiz-game/
├── app.py                    # Main Streamlit app
├── requirements.txt          # Dependencies
│
├── config/
│   └── settings.py          # Centralized configuration
│
├── services/                # Core business logic
│   ├── llm_service.py      # LLM routing & management
│   ├── user_service.py     # User auth & tracking
│   ├── gamification.py     # Points/levels/badges
│   └── progress_service.py # Data persistence
│
├── utils/
│   └── prompts.py          # LLM prompt templates
│
├── data/
│   └── users.json          # User data (auto-created)
│
├── docs/
│   ├── SETUP.md            # Installation guide
│   ├── ARCHITECTURE.md     # System design
│   └── FEATURES.md         # Feature documentation
│
└── .env                     # Environment variables
```

---

## 🎯 Gamification System

### Points & Levels

```
Base Points:         10 points per correct answer
Streak Bonus:        +5 points for every 3 consecutive correct
Perfect Quiz:        1.5x multiplier (all answers correct)

Example (5 questions, 4 correct):
  → 4 × 10 = 40 points
  → Streak bonus (3 consecutive) = +5 points
  → Total: 45 points
```

### 5-Level Progression

```
Level 1 (0-49)      🥉 Quiz Starter
Level 2 (50-99)     📚 Learning Enthusiast
Level 3 (100-199)   🧠 Concept Explorer
Level 4 (200-399)   🎯 Knowledge Seeker
Level 5 (400+)      🏆 Quiz Champion
```

### 5 Collectible Badges

```
🥉 Quiz Starter      → Reach 50 points
🧭 Concept Explorer  → Learn 10 different topics
🥈 Concept Master    → Reach 200 points
🔥 Streak Champ      → Achieve 10-answer correct streak
🥇 Quiz Champion     → Reach 500 points
```

---

## 🔐 Security & Data

### User Authentication
- SHA-256 password hashing (industry standard)
- Per-user data isolation
- Session-based tracking
- No plain-text password storage

### Data Privacy
- All data stored locally in `data/` folder
- No cloud transmission
- Full user control
- Easy backup and export

---

## ✅ What's Actually Implemented

- ✅ User authentication (register/login with SHA-256)
- ✅ Ask the Tutor (AI explanations via Ollama)
- ✅ Generate Quiz (AI-created MCQ questions)
- ✅ Gamification (points, levels, badges, streaks)
- ✅ Progress Dashboard (stats & history)
- ✅ Global Leaderboard (user rankings)
- ✅ Response Caching (MD5-based)
- ✅ Dual LLM Providers (Ollama primary, Gemini fallback)
- ✅ Answer Evaluation & Feedback
- ✅ Per-user Data Isolation

---

## ❌ What's NOT Implemented

- ❌ Adaptive difficulty (levels are fixed, not adaptive)
- ❌ Video explanations
- ❌ Mobile app (web-only, works on all browsers)
- ❌ Advanced analytics dashboard
- ❌ Community sharing features
- ❌ Voice-based interactions

---

## 🐛 Troubleshooting

### Ollama Issues

**"Ollama not responding"**
- Ensure Ollama is installed and running
- Run: `ollama serve`

**"Model not found"**
- Pull the model: `ollama pull neural-chat`
- Check available models: `ollama list`

**"Slow responses (>45 seconds)"**
- Check system resources
- Try faster model: `ollama pull orca-mini`
- Adjust timeout in `config/settings.py`

### Data Issues

**"Quiz answers not saving"**
- Check write permissions on `data/` folder
- Ensure JSON files aren't corrupted
- Delete `data/users.json` to reset

**"Port 8501 already in use"**
- Run on different port: `streamlit run app.py --server.port 8502`

---

## 📚 Documentation

- **[SETUP.md](docs/SETUP.md)** - Detailed installation & troubleshooting
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design & data flow
- **[FEATURES.md](docs/FEATURES.md)** - Feature breakdown & usage
- **[config/settings.py](config/settings.py)** - Configuration options

---

## 🔄 How It Works

1. **User registers** → Account created with hashed password
2. **Asks tutor** → LLMService routes to Ollama → Response cached
3. **Takes quiz** → AI generates questions → User answers
4. **Gets feedback** → AI evaluates answers → Points awarded
5. **Progress tracked** → Gamification engine updates stats
6. **Data persisted** → Saved to `data/users.json`
7. **Ranks calculated** → Leaderboard updated in real-time

---

## 💡 Key Technical Achievements

### 1. Dual-Provider LLM Architecture
- Primary: Ollama (local, free, offline)
- Fallback: Gemini (when available)
- Intelligent error handling

### 2. Complete User Management
- Secure authentication (SHA-256)
- Per-user data isolation
- Persistent accounts & progress

### 3. Advanced Gamification
- 5-level progression system
- 5 collectible badges
- Streak mechanics
- Real-time accuracy tracking
- Multi-player leaderboard

### 4. Production-Grade Code
- Service-oriented architecture
- Modular design
- Error handling & validation
- Response caching
- Clean documentation

### 5. Offline-First Design
- Works completely offline (Ollama)
- No cloud dependency
- Local data storage
- Fallback to cloud if available

---

## 📊 Comparison

| Feature | This Project | ChatGPT API | Traditional Tutoring |
|---------|-------------|-------------|----------------------|
| **Cost** | FREE | $0.01-0.03 per request | $30-100/hour |
| **Offline** | ✅ Yes | ❌ No | N/A |
| **Speed** | 10-30s | 2-5s | Real-time |
| **Gamification** | ✅ Full | ❌ None | ❌ None |
| **User Tracking** | ✅ Yes | ❌ No | Per-session |
| **Data Privacy** | ✅ Local | ❌ Cloud | Local |
| **Leaderboard** | ✅ Yes | ❌ No | ❌ No |

---

## 🚀 Getting Started

### For Users
1. Install Ollama → `ollama pull neural-chat`
2. Install project → `pip install -r requirements.txt`
3. Run app → `streamlit run app.py`
4. Register account and start learning!

### For Developers
1. Review `ARCHITECTURE.md` for system design
2. Check `config/settings.py` for configuration
3. Explore `services/` for business logic
4. Modify prompts in `utils/prompts.py`

---

## 📝 License

MIT License - Free to use, modify, and distribute

---

## 📞 Support

- **Installation help?** → See [docs/SETUP.md](docs/SETUP.md)
- **System design?** → See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Feature details?** → See [docs/FEATURES.md](docs/FEATURES.md)
- **Configuration?** → See [config/settings.py](config/settings.py)

---

**Made with ❤️ for learners everywhere**

**Status**: ✅ Fully Functional | **Tech Stack**: Streamlit + Ollama + Python  
**GitHub**: [quiz-game](https://github.com/YOUR_USERNAME/quiz-game) | **Last Updated**: March 2026

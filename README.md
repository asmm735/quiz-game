# 🎓 AI Quiz Tutor - Interactive Learning Platform

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.55.0-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-412991?logo=github&logoColor=white)](https://ollama.ai)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 A Complete AI-Powered Learning Ecosystem

**AI Quiz Tutor** is a production-grade educational platform that demonstrates modern software engineering practices. It combines:
- **🤖 AI-Powered Explanations** (via Ollama locally, with Gemini as fallback)
- **🎯 Intelligent Quiz Generation** (with difficulty levels)
- **🎮 Advanced Gamification** (points, levels, badges, streaks)
- **📊 Real-Time Progress Tracking** (per-user analytics)
- **⚡ Zero Cost Operation** (Ollama - completely local & free)

### **Key Project Achievements**
✅ **Full-stack development** - Frontend, backend, data layer  
✅ **Service-oriented architecture** - Modular, maintainable code  
✅ **User authentication & tracking** - Per-user data isolation  
✅ **Smart LLM integration** - Auto-detection, caching, fallbacks  
✅ **Gamification mechanics** - Points, levels, badges, streaks  
✅ **Production-ready error handling** - Validation, retries, graceful fallbacks  

---

## ✨ Feature Showcase

### 💡 **Ask the Tutor** - Intelligent Explanations
Receive detailed AI explanations with:
- Real-world analogies and practical examples
- Key learning points summary
- Follow-up questions to verify understanding
- Interesting facts and context
- **Speed**: 10-30 seconds per explanation (local neural-chat model)

### 📝 **Generate Quiz** - AI-Powered Assessment
AI-generated quizzes with:
- Multiple difficulty levels (Easy, Medium, Hard)
- AI-generated multiple choice questions
- Detailed explanations for answers
- Learn from mistakes with "Explain Wrong Answer" feature
- **Smart Scoring**: 10 points per correct + 5 bonus per 3-streak
- **Speed**: 20-120 seconds per quiz (depending on question count)

### 🎮 **Gamification Engine** - Complete Point System
Engagement through game mechanics:
```
Points:     10 per correct answer + 5 per 3-correct streak
Levels:     1-5 progression (0 → 400+ points)
Badges:     5 collectible milestones
Streaks:    Current + personal best tracking
Accuracy:   Real-time performance metrics
```

### 📊 **Progress Dashboard** - Analytics Hub
Track every metric that matters:
- Total points and level progression
- Quiz history with scores and dates
- Accuracy percentage per topic
- Current and best streak visualization
- Badge achievements display

### 🏆 **Global Leaderboard** - Social Engagement
Competitive ranking system:
- User rankings by points
- Performance comparisons
- Milestone celebrations
- Real-time updates

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai) (free, local LLM runtime)
- Optional: Google API key for Gemini (as fallback LLM)

### 2. Installation
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/quiz-game.git
cd quiz-game

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 3. Setup Ollama
```bash
# Download and install Ollama from https://ollama.ai

# Pull the fast neural-chat model
ollama pull neural-chat

# Verify it's working
curl http://localhost:11434/api/tags
```

### 4. Run the App
```bash
streamlit run app.py
```

App opens at **http://localhost:8501** 🎉

---

## 🛠️ Technical Architecture (What Makes This Stand Out)

### **Service-Oriented Design**
Clean separation of concerns with modular services:

| Component | Responsibility | Technology |
|-----------|-----------------|-----------|
| **LLMService** | AI interactions, response caching, timeout management | Ollama + neural-chat |
| **UserService** | Authentication, per-user tracking, data isolation | SHA-256 hashing, JSON |
| **GamificationEngine** | Points, levels, badges, streaks calculation | Custom logic |
| **ProgressStore** | Data persistence, quiz history | JSON files |

### **Smart LLM Integration**
```
⚡ Primary: Ollama (neural-chat model)
   - Completely local & free
   - 10-30 seconds per response
   - Works offline

📡 Fallback: Google Gemini (if API key provided & available)
   - Used when Ollama unavailable
   - Requires GOOGLE_API_KEY in .env

Advanced Features:
✅ Dual-provider router      (Ollama first, Gemini fallback)
✅ Auto-model detection      (neural-chat → orca-mini → available)
✅ Response caching          (MD5-based, prevents regeneration)
✅ Intelligent timeouts      (45s explain, 120s quiz, 60s eval)
✅ Retry mechanism           (2 retries on timeout)
✅ Validation layers         (quality checks, placeholder rejection)
✅ Graceful fallbacks        (returns None instead of fake answers)
```

### **Performance Metrics**
```
Cold Start:          ~45 seconds (Ollama model initializing)
Warm Responses:      10-30 seconds (neural-chat model)
Cached Hits:         <1 second (in-memory cache)
Total Quiz Time:     2-3 minutes (5 questions)
```

### **LLM Provider Selection**
```
User Request
    ↓
LLMService Router checks availability
    ├─→ Ollama available? YES → Use Ollama (primary)
    ├─→ Ollama unavailable? NO → Try Gemini (fallback)
    └─→ Both unavailable? NO → Return error (no fake answers)
    ↓
Response Parsing & Validation
    ↓
MD5 Cache Check
    ↓
Display to User & Update UserService
    ↓
GamificationEngine Updates Points/Badges
    ↓
Persist to data/users.json
```

### **Current Status**
- **LLM Provider**: Ollama (neural-chat model) - Free & Local ✅
- **Gemini**: Available as fallback (requires API key in .env)
- **Note**: Ollama is primary choice because it's completely free and works offline

---

## 🎯 Key Technical Achievements

### **1. Dual-Provider LLM Architecture** 🤖
- **Primary**: Ollama (local, free, offline)
- **Fallback**: Google Gemini (when API available)
- Intelligent routing with error handling
- Zero cost when using Ollama

### **2. Complete User Management System** 👥
- Secure authentication (SHA-256 hashing)
- Per-user data isolation
- Persistent user accounts
- Session-based tracking

### **3. Advanced Gamification System** 🎮
- 5-level progression (0-500+ points)
- 5 collectible badges with meaningful achievements
- Streak tracking (current + personal best)
- Real-time accuracy metrics
- Global leaderboard

### **4. Production-Grade Code Quality** 🏭
- Service-oriented architecture (4 independent services)
- Modular design - easy to extend
- Error handling - timeouts, retries, validation
- Response caching - prevents regeneration
- Clean folder structure & documentation

### **5. Smart Offline-First Design** ⚡
- Works completely offline (Ollama)
- No cloud dependency
- Local data storage (JSON files)
- Fallback to cloud (Gemini) if configured

---

## 📊 Performance Comparison

| Feature | This Project | Basic LLM | Expensive API |
|---------|-------------|-----------|---------------|
| **Cost** | FREE | Free | $0.01-0.03 per request |
| **Speed** | 10-30s | Same | Depends |
| **Offline** | ✅ Yes | ✅ Yes | ❌ No |
| **Gamification** | ✅ Full | ❌ None | ❌ None |
| **User Tracking** | ✅ Per-user | ❌ None | ⚠️ Limited |
| **Data Privacy** | ✅ Local only | ✅ Local | ❌ Cloud stored |
| **Customization** | ✅ Full | Medium | Low |

---

## 📁 Clean, Organized Project Structure

```
quiz-game/
├── app.py                          ← Main Streamlit app
├── requirements.txt                ← Dependencies
│
├── 🔧 config/
│   └── settings.py        Chat GPT API | Traditional Tutoring |
|---------|-------------|---------------|----------------------|
| **Cost** | FREE (Ollama) | $0.01-0.03 per request | $30-100/hour |
| **Speed** | 10-30s (local) | 2-5s (cloud) | Real-time |
| **Works Offline** | ✅ Yes (Ollama) | ❌ No | N/A |
| **Gamification** | ✅ Full system | ❌ None | ❌ None |
| **User Tracking** | ✅ Per-user analytics | ❌ None | Per-session |
| **Data Privacy** | ✅ Local only | ❌ Cloud stored | Local |
| **Customization** | ✅ Full | Low | High (manual) |
| **Leaderboard** | ✅ Multi-user | ❌ No | ❌ No
│   └── prompts.py                 ← LLM prompt templates
│
├── 📖 docs/                       ← Comprehensive documentation
│   ├── SETUP.md                   ← Installation guide
│   ├── ARCHITECTURE.md            ← System design
│   └── FEATURES.md                ← Feature documentation
│
├── 💾 data/                       ← User data storage
│   └── users.json                 ← Auto-created at runtime
│
└── 🔒 .env                        ← Environment variables
```

Every folder has a clear purpose - easy to navigate!

---

## 📚 Documentation

See detailed docs in the `docs/` folder:

- **[SETUP.md](docs/SETUP.md)** - Detailed installation and troubleshooting
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and component overview
- **[FEATURES.md](docs/FEATURES.md)** - Complete feature documentation
- **[config/settings.py](config/settings.py)** - All configurable parameters

## 📁 Project Structure

```
quiz-game/
├── app.py                      # 🎯 Main Streamlit application
├── requirements.txt            # Python dependencies
├── config/
│   └── settings.py            # 🔧 Centralized configuration
├── services/
│   ├── llm_service.py         # 🤖 LLM interactions
│   ├── user_service.py        # 👤 User authentication
│   ├── gamification.py        # 🎮 Points/levels/badges
│   └── progress_service.py    # 📊 Progress persistence
├── utils/
│   └── prompts.py             # 📝 LLM prompt templates
├── data/
│   └── users.json             # 💾 User data (auto-created)
├── docs/
│   ├── SETUP.md               # Setup instructions
│   ├── ARCHITECTURE.md        # System design
│   └── FEATURES.md            # Feature documentation
└── venv/                       # Virtual environment
```

## 🎮 How to Use

### 1. Register/Login
- Create unique account with secure password
- Per-user data isolation and tracking
- Session-based authentication

### 2. Ask the Tutor
- Enter any topic ("Python exceptions", "photosynthesis", etc.)
- Get instant AI explanation with real-world analogies and examples
- Responses are cached for faster subsequent access

### 3. Generate Quiz
- Select topic, difficulty (Easy/Medium/Hard), and question count
- AI creates structured MCQ questions
- Take the quiz and get instant feedback
- Learn from explanations for wrong answers

### 4. Track Progress
- View your points, level, badges, and streak
- Check quiz history and accuracy
- See your ranking on global leaderboard

## 🎯 Gamification System Deep Dive

### 📈 Points Architecture
```
Base Points:        10 points per correct answer
Streak Bonus:       +5 points for every 3 consecutive correct
Perfect Quiz:       1.5x multiplier (all answers correct)

Example:
  Quiz with 5 questions (4 correct, 1 incorrect):
  → 4 × 10 = 40 points
  → Streak bonus (3 consecutive) = +5 points
  → Total: 45 points
```

### 🏅 Level Progression
```
Level 1 (0-49)      🥉 Quiz Starter
Level 2 (50-99)     📚 Learning Enthusiast
Level 3 (100-199)   🧠 Concept Explorer
Level 4 (200-399)   🎯 Knowledge Seeker
Level 5 (400+)      🏆 Quiz Champion
```

### 🎖️ Badge System (5 Collectibles)
```
🥉 Quiz Starter        → Reach 50 points
🧭 Concept Explorer    → Learn 10 different topics
🥈 Concept Master      → Reach 200 points
🔥 Streak Champ        → Achieve 10-answer correct streak
🥇 Quiz Champion       → Reach 500 points
```

---

## 🔐 Security & Data

### Authentication
- SHA-256 password hashing (industry standard)
- Per-user data isolation
- Secure session management
- No plain-text password storage

### Data Privacy
- All data stored locally (data/ folder)
- No cloud transmission
- Full user control
- Easy backup and export

---

## 📈 Future Improvements

- [ ] Support for multiple languages
- [ ] Mobile app version
- [ ] Advanced analytics dashboard
- [ ] Customizable difficulty adaptation
- [ ] Video explanations
- [ ] Community sharing of quizzes
- [ ] Export progress as PDF report
- [ ] Multiplayer quiz challenges

---

## 📝 License

MIT License - Feel free to use for educational and commercial purposes

---

## 🤝 Contributing

Contributions welcome! Ways to contribute:
1. Report bugs and suggest features
2. Improve documentation
3. Add new gamification mechanics
4. Optimize performance
5. Create educational content

---

## 📧 Support & Documentation

For help and more information:

- **Setup Issues?** → Check [SETUP.md](docs/SETUP.md)
- **Want to understand architecture?** → Read [ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **Need feature details?** → See [FEATURES.md](docs/FEATURES.md)
- **Configuration help?** → Review [config/settings.py](config/settings.py)

---

## ✨ Project Summary

**AI Quiz Tutor** demonstrates:
- ✅ Full-stack web application development
- ✅ Service-oriented architecture patterns
- ✅ User authentication & data persistence
- ✅ Advanced gamification mechanics
- ✅ AI/LLM integration & optimization
- ✅ Clean code practices & documentation
- ✅ Production-grade error handling

This is more than just a homework project—it's a **complete, production-ready learning platform** that you can deploy, customize, and scale.

---
## 🐛 Known Limitations & Troubleshooting

### Ollama Issues
- **"Ollama not responding"** → Ensure Ollama is installed and running (`ollama serve`)
- **"Model not found"** → Pull model: `ollama pull neural-chat`
- **"Slow responses"** → Ollama is slower than cloud APIs but free and offline

### Data Issues
- **Quiz answers not saving** → Check write permissions on `data/` folder
- **JSON files corrupted** → Delete `data/users.json` and re-register accounts
- **Cache issues** → Clear browser cache in Streamlit settings

### Performance
- **First response slow** → Normal - model is initializing (45 seconds)
- **Subsequent responses slow** → Check system resources or reduce timeout in settings
- **Port 8501 in use** → Run on different port: `streamlit run app.py --server.port 8502`

---

## 📊 What's Actually Implemented ✅

- ✅ User authentication (register/login with SHA-256 hashing)
- ✅ Ask the Tutor (AI explanations via Ollama)
- ✅ Generate Quiz (AI-created MCQ questions)
- ✅ Gamification (points, levels, badges, streaks)
- ✅ Progress Dashboard (stats & history)
- ✅ Global Leaderboard (user rankings)
- ✅ Response Caching (MD5-based)
- ✅ Dual LLM providers (Ollama primary, Gemini fallback)
- ✅ Answer evaluation & feedback
- ✅ Per-user data isolation

---

## 📋 What's NOT Implemented

- ❌ Adaptive difficulty (difficulty levels are fixed, not adaptive)
- ❌ Video explanations
- ❌ Mobile app (web-only via Streamlit)
- ❌ Advanced analytics dashboard
- ❌ Community sharing features
- ❌ Integration with external educational APIs
- ❌ Voice-based interactions

---

## ✨ Project Summary

**AI Quiz Tutor** demonstrates:
## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with valid API key and internet connection

---

**Happy Learning! 🚀**

Built with ❤️ using Streamlit, OpenAI, and Python
#   q u i z - g a m e 
 
 ---

**Made with ❤️ for learners everywhere**

**GitHub**: [quiz-game](https://github.com/YOUR_USERNAME/quiz-game)  
**Status**: ✅ Fully Functional & Tested  
**Last Updated**: March 2026  
**Tech Stack**: Streamlit + Ollama + Python + JSON

---

## 📞 Questions?

- **Setup Help**: See [docs/SETUP.md](docs/SETUP.md)
- **Architecture Details**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)  
- **Feature Breakdown**: See [docs/FEATURES.md](docs/FEATURES.md)
- **Configuration**: See [config/settings.py](config/settings.py)

Enjoy learning! 🚀
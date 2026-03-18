# 📖 Getting Started - Complete Setup Guide

Welcome to AI Quiz Tutor! This guide will get you up and running in 5 minutes.

## ✅ Pre-Flight Checklist

- [ ] Python 3.8 or higher installed
- [ ] OpenAI API account (free tier with $5 credit available)
- [ ] Internet connection
- [ ] Text editor or IDE

## 📝 Step-by-Step Setup

### Step 1: Get Your API Key (2 minutes)

1. Go to: https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. **Important:** Save it - you won't see it again!

### Step 2: Configure Environment (1 minute)

In the `quiz-game` folder, create a file named `.env`:

**Option A: Copy from template**
```bash
cp .env.example .env
```

**Option B: Manually create:**
1. Create a new file named `.env` in the `quiz-game` folder
2. Add this line:
```
OPENAI_API_KEY=sk_your_api_key_here
```
3. Replace `sk_your_api_key_here` with your actual key

### Step 3: Install Dependencies (1 minute)

Open terminal/command prompt in the `quiz-game` folder:

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web interface
- `openai` - API client
- `python-dotenv` - Environment variable management

### Step 4: Run the App! (1 minute)

```bash
streamlit run app.py
```

The app opens at: `http://localhost:8501`

You should see:
- Welcome screen with 4 sections
- Quick stats sidebar
- Navigation menu

---

## 🎬 First Time Using the App

### Home Page (Read Overview)
- See what each feature does
- View your quick stats
- Understand the gamification system

### 💡 Ask the Tutor (Start Here!)

1. Click "Ask the Tutor"
2. Type something like:
   - "Explain recursion simply"
   - "What is machine learning?"
   - "Teach me Python list comprehensions"
3. Click "Get Explanation"
4. See:
   - Simple explanation
   - Real-world analogy
   - Key points
   - Follow-up question
   - Fun fact

### 📝 Take a Quiz

1. Click "Generate Quiz"
2. Enter:
   - **Topic:** (e.g., "Recursion")
   - **Difficulty:** Easy (start here!)
   - **Questions:** 5
3. Click "Generate Quiz"
4. Answer all questions
5. Click "Submit Quiz"
6. See your score and explanations
7. Optionally click "Explain why I got this wrong" for deeper learning

### 📊 View Progress

1. Click "Progress Dashboard"
2. See:
   - Total points earned
   - Current level
   - Quiz history
   - Badge collection

---

## 🎮 Understanding Gamification

### Points
- **+10** points for each correct answer
- **+5** bonus points every 3 correct answers in a row
- Points accumulate for life

### Levels
```
Level 1: 0-49 points      (Quiz Starter)
Level 2: 50-99 points
Level 3: 100-199 points   (Concept Master!)
Level 4: 200-399 points
Level 5: 400+ points      (Quiz Champion!)
```

### Streaks
- **Correct answer** = streak +1
- **Wrong answer** = streak resets to 0
- Every 3 correct in a row = bonus points!

### Badges
You earn badges for achievements:
- **Quiz Starter**: 50 points
- **Concept Explorer**: 10 different topics
- **Concept Master**: 200 points
- **Streak Champ**: 10 correct in a row
- **Quiz Champion**: 500 points

---

## 🆘 Troubleshooting

### "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit openai python-dotenv
```

### "OPENAI_API_KEY not found"
**Solutions:**
1. Check `.env` file exists in project root
2. Verify format: `OPENAI_API_KEY=sk_xxx...`
3. Restart the app
4. Try: `pip install python-dotenv` again

### "Failed to generate quiz"
**Possible causes:**
1. No internet connection
2. API key is invalid or has no credits
3. API being rate-limited

**Solution:**
1. Check: https://status.openai.com/
2. Verify key on: https://platform.openai.com/account/api-keys
3. Check billing: https://platform.openai.com/account/billing/overview

### "Streamlit is already running"
**Solution:**
```bash
# Kill the process
Ctrl+C in terminal

# Then restart
streamlit run app.py
```

### "Port 8501 already in use"
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502
```

---

## 🎯 Sample Learning Path

### Day 1 (30 minutes)
1. Install and run app ✅
2. Ask tutor: "Explain machine learning basics"
3. Take easy quiz: "Machine Learning"
4. Earn ~50 points
5. View progress

### Day 2 (30 minutes)
1. Ask tutor: "What is supervised learning?"
2. Take medium quiz: "Regression"
3. Earn ~100 points total
4. Level up to Level 2! 🎉
5. Check dashboard for recent topics

### Day 3 (30 minutes)
1. Ask tutor: "Deep explanation of neural networks"
2. Take hard quiz: "Neural Networks"
3. Maintain 10+ correct streak
4. Earn 500+ total points
5. Unlock badges!

---

## 📚 Features Explained

### Ask the Tutor
- **Use when:** Learning a new concept
- **Maximum daily:** No limit
- **Time per question:** 2-5 seconds
- **Output:** Explanation + analogy + key points

### Generate Quiz
- **Use when:** Testing understanding
- **Questions:** 3-10 per quiz
- **Time per quiz:** 5-15 minutes
- **Output:** Score, feedback, explanations

### Progress Dashboard
- **Use when:** Tracking progress
- **Shows:** Points, levels, badges, accuracy
- **History:** All past quizzes with scores
- **Frequency:** Check weekly for motivation

---

## 💡 Pro Tips

### For Learning Effectively
1. **Use tutor first** before taking quiz on a topic
2. **Start with easy** difficulty
3. **Read explanations** for wrong answers carefully
4. **Build streaks** for bonus points
5. **Explore variety** of topics to unlock badges

### For Better Results
- 🎯 Focus on one topic per session
- ✍️ Take notes while using tutor
- 🔁 Retry failed quizzes at higher difficulty
- 📊 Review dashboard weekly
- 🏆 Aim for badges as goals

### For Maximizing Points
- 10 points per correct answer
- 5 points bonus every 3 correct
- Maximum 15 points per question if streak active!
- Focus on accuracy over speed

---

## 🔧 Customization (Optional)

You can customize:

### 1. Points system
Edit `services/gamification.py`:
```python
POINTS_PER_CORRECT = 10  # Change this
STREAK_BONUS = 5         # Or this
```

### 2. Difficulty levels
Edit `services/llm_service.py` to change what "easy", "medium", "hard" mean for your domain

### 3. Number of levels
Edit `services/gamification.py`:
```python
LEVEL_THRESHOLDS = {
    1: (0, 49),
    2: (50, 99),
    3: (100, 199),
    4: (200, 399),
    5: (400, float('inf'))
}
```

See [CONFIGURATION.md](CONFIGURATION.md) for more options!

---

## 📊 Data Storage

Your progress is saved in:
- `data/student_progress.json` - Your stats
- `data/quiz_history.json` - All quiz attempts

**Backup these files to save your progress!**

---

## 🚀 Ready to Go?

1. ✅ API key configured
2. ✅ Dependencies installed
3. ✅ App running: `streamlit run app.py`
4. ✅ Visit: http://localhost:8501

Start with "Ask the Tutor" for a topic you want to learn!

---

## 📞 Need Help?

- **Setup issues**: Check `.env` file first
- **Feature questions**: See [README.md](README.md)
- **Customization**: See [CONFIGURATION.md](CONFIGURATION.md)
- **Architecture details**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Quick start**: See [QUICKSTART.md](QUICKSTART.md)

---

## 🎓 Happy Learning!

You're all set. Start learning with AI! 🚀

**Next step:** Open app and ask tutor about something you're curious about!

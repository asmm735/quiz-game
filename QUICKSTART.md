# 🚀 Quick Start Guide

## 1️⃣ Setup (2 minutes)

```bash
# Step 1: Navigate to project folder
cd quiz-game

# Step 2: Install dependencies
pip install -r requirements.txt

# Step 3: Get your OpenAI API key
# Sign up at https://platform.openai.com/
# Copy your API key

# Step 4: Create .env file
# Option A: Copy from template
cp .env.example .env

# Option B: Create manually
# Create a file named '.env' with this content:
# OPENAI_API_KEY=your_key_here_sk_xxxx...
```

## 2️⃣ Run (1 command)

```bash
streamlit run app.py
```

The app opens at: `http://localhost:8501`

## 3️⃣ Use (Start Here!)

### 🎓 First Time? Go Home!
- See overview of all features
- Check your quick stats

### 💡 Ask the Tutor First
1. Type: "Explain recursion simply"
2. Get AI explanation with analogy
3. See key points and follow-up question

### 📝 Then Take a Quiz
1. Topic: "Recursion"
2. Difficulty: "Easy" (start easy!)
3. Questions: "5"
4. Click: "Generate Quiz"
5. Answer and submit

### 📊 Check Your Progress
- See your points: 0 → 10 → 20...
- Level up as you earn points
- Earn badges for milestones
- Track recent topics

---

## 🎮 Points System

| Action | Points |
|--------|--------|
| Correct answer | +10 |
| 3 in a row | +5 bonus |
| Level up | Achievement! |
| Badge earned | Trophy! |

---

## 💡 Pro Tips

1. **Start Easy**: Begin with easy difficulty, then move up
2. **Use Tutor First**: Ask the tutor for tough topics before quizzing
3. **Learn from Mistakes**: Click "Explain my wrong answers"
4. **Build Streaks**: Try to maintain a streak for bonus points
5. **Explore Topics**: Study varied topics to unlock "Concept Explorer" badge

---

## 🆘 Help

**API Key Error?**
- Make sure `.env` file is in same folder as `app.py`
- Check key format: `OPENAI_API_KEY=sk_...`
- Restart app after creating `.env`

**Quiz not generating?**
- Check internet connection
- Verify API key is valid
- Check OpenAI credits/billing

**Progress not saving?**
- `data/` folder should be auto-created
- Check folder has write permissions

---

## 📚 Files Created

The app creates these files automatically:

```
quiz-game/
├── data/
│   ├── student_progress.json  ← Student stats
│   └── quiz_history.json      ← Quiz attempts
```

**Backup these files to save your progress!**

---

## 🔌 API Keys Info

### Getting an OpenAI API Key
1. Visit: https://platform.openai.com/account/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Paste into `.env` file

### Cost
- GPT-3.5 is cheap (~$0.001 per 1K tokens)
- Average quiz: ~100 tokens
- Average explanation: ~150 tokens
- Free tier: $5 credit included

---

## 🎬 Demo Flow

**Minute 1-2: Setup**
- Install, create `.env`, run app

**Minute 3-5: Test Feature 1 - Ask Tutor**
- Ask about any topic
- See explanation, analogy, key points

**Minute 5-8: Test Feature 2 - Quiz**
- Generate 5-question quiz
- Answer and see score
- Review explanations

**Minute 8-9: Test Feature 3 - Gamification**
- See points earned
- Check current level
- View badges

**Minute 9-10: Test Feature 4 - Dashboard**
- See all stats
- Review quiz history
- Check progress

**Total Demo Time: ~10 minutes**

---

## 📞 Troubleshooting Checklist

- [ ] Python 3.8+ installed? (`python --version`)
- [ ] Dependencies installed? (`pip list | grep streamlit`)
- [ ] `.env` file created with API key?
- [ ] Key format correct? (`OPENAI_API_KEY=sk_...`)
- [ ] Running from correct folder? (where `app.py` is)
- [ ] Internet connection working?
- [ ] OpenAI account has credits?

---

## 🎯 Next Steps

1. ✅ Complete setup
2. ✅ Run first quiz
3. ✅ Earn first badge
4. ✅ Hit 100 points
5. ✅ Reach Level 3!

---

**Ready? Let's go! 🚀**

```bash
streamlit run app.py
```

Enjoy learning! 🎓

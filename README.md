# 🎓 AI Quiz Tutor - Interactive Learning Platform

A Streamlit-based educational AI tutor app that combines concept explanation, quiz generation, gamification, and progress tracking.

## ✨ Features

### 1. **Ask the Tutor** 💡
- Enter any topic or question
- Get simple, clear explanations with:
  - Real-world analogies
  - Key points summary
  - Follow-up questions to check understanding
  - Fun facts related to the topic

### 2. **Generate Quiz** 📝
- Select topic, difficulty level, and number of questions
- AI generates structured MCQ questions
- Immediate feedback and explanations
- "Explain my wrong answers" feature for deeper learning
- Adaptive difficulty based on performance

### 3. **Gamification System** 🎮
- **Points**: +10 points per correct answer
- **Streak Bonus**: +5 points for every 3 correct answers in a row
- **Levels**: Progress through 5 levels (0-49, 50-99, 100-199, 200-399, 400+)
- **Badges**: Earn badges for milestones
  - Quiz Starter (50 points)
  - Concept Explorer (10 topics)
  - Concept Master (200 points)
  - Streak Champ (10 correct streak)
  - Quiz Champion (500 points)

### 4. **Progress Dashboard** 📊
- View total points, current level, and badges
- Track quiz accuracy percentage
- See recent topics studied
- Monitor current streak and best streak
- Complete quiz history

## 🏗️ Architecture

```
User Interface (Streamlit)
    ↓
Concept Engine → LLM API (Explanations)
Quiz Engine → LLM API (Question Generation)
Evaluation Engine → LLM (Answer Feedback)
Gamification Engine → Updates Points, Levels, Badges
Progress Store → JSON/SQLite Storage
```

## 🚀 Quick Setup

### 1. Prerequisites
- Python 3.8+
- OpenAI API Key (or compatible LLM API)

### 2. Installation

```bash
# Clone/Download the project
cd quiz-game

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-xxxxxxxxxxxx
```

### 3. Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📋 Project Structure

```
quiz-game/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
├── services/
│   ├── __init__.py
│   ├── llm_service.py        # LLM API interactions (explanations, quizzes, evaluation)
│   ├── gamification.py        # Points, levels, streaks, badges
│   └── progress_service.py    # Student progress storage and retrieval
└── data/
    ├── student_progress.json  # Persisted student data (auto-created)
    └── quiz_history.json      # Quiz attempt history (auto-created)
```

## 💻 How to Use

### Starting Out
1. **Home Page**: Overview of features and your quick stats
2. **Ask the Tutor**: Search for any topic to get AI explanations
3. **Generate Quiz**: Create custom quizzes based on difficulty
4. **Dashboard**: Track your progress and achievements

### Taking a Quiz
1. Enter a topic (e.g., "Python recursion")
2. Choose difficulty: Easy, Medium, or Hard
3. Select 3-10 questions
4. Answer all questions
5. Review results with explanations
6. Click "Explain my wrong answers" for deeper understanding

### Earning Points
- ✅ **10 points** per correct answer
- 🔥 **5 bonus points** after 3 correct in a row
- 📊 **Level up** as you accumulate points
- 🏅 **Badges** awarded for milestones

### Adaptive Learning
- Quizzes below 40% suggest easier difficulty
- Quizzes above 80% encourage harder difficulty
- System tracks your performance and suggests topics

## 🔑 Key Prompts Used

### Concept Explanation Prompt
```
You are a friendly student-friendly tutor. 
Explain [TOPIC] in very simple language.
Provide: simple explanation, real-world analogy, key points, follow-up question, fun fact
```

### Quiz Generation Prompt
```
Generate [N] MCQs about [TOPIC] at [DIFFICULTY] level.
Return structured JSON with:
- Question text
- 4 options (exactly 1 correct)
- Explanation
```

### Answer Evaluation Prompt
```
Evaluate the student's answer and provide:
- Is it correct?
- Score (0-100)
- Explanation
- Improvement tip
- Related concept to learn
```

## 🎯 Personalization Features

1. **Adaptive Difficulty**
   - Below 40%: Next quiz becomes easier
   - 40-80%: Maintain difficulty
   - Above 80%: Next quiz harder

2. **Topic Tracking**
   - System remembers which topics you've studied
   - Suggests related topics
   - Shows recent study history

3. **Performance-Based Feedback**
   - Different messages for different score ranges
   - Custom improvement suggestions
   - Detailed explanations for mistakes

## 📊 Data Persistence

All your progress is saved locally in JSON files:
- **student_progress.json**: Overall stats, gamification data, preferences
- **quiz_history.json**: Complete history of all quiz attempts

You can backup these files or export them for analysis.

## 🔧 Configuration

### LLM Service
- **Default Model**: GPT-3.5-turbo (cost-effective)
- **Temperature**: 0.7 for explanations, 0.5 for evaluations
- Change model in `services/llm_service.py`

### Gamification Constants
Edit in `services/gamification.py`:
- Points per correct answer: `POINTS_PER_CORRECT = 10`
- Streak bonus threshold: `STREAK_THRESHOLD = 3`
- Badge thresholds and level ranges

## 🚀 Deployment Options

### Streamlit Cloud (Recommended)
```bash
# Push to GitHub, then deploy from Streamlit Cloud dashboard
```

### Hugging Face Spaces
- Create a Space
- Connect your GitHub repo
- Add secrets for API keys

### Render / Railway
- Deploy Docker container
- Set environment variables
- Scale as needed

## 📱 Mobile Support
The app is fully responsive and works on mobile devices. Use Streamlit's mobile-optimized layout.

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Check `.env` file exists in project root
- Verify key format: `OPENAI_API_KEY=sk-...`
- Restart the app

### "Failed to generate quiz"
- Check API rate limits
- Verify internet connection
- Ensure API key has sufficient credit

### Quiz answers not saving
- Check `data/` folder has write permissions
- Ensure JSON files aren't corrupted
- Clear cache: `streamlit cache clear`

## 🎓 Educational Best Practices

This app implements:
- ✅ Active recall through quizzes
- ✅ Spaced repetition (quiz history tracking)
- ✅ Elaborative interrogation ("explain why" feature)
- ✅ Immediate feedback (explanations after each question)
- ✅ Gamification (points, badges, levels)
- ✅ Adaptive difficulty (based on performance)

## 📈 Future Enhancements

Nice-to-have features (not in MVP):
- [ ] Multi-user support with authentication
- [ ] Leaderboards and social features
- [ ] RAG with custom study materials
- [ ] Voice-based questions/answers
- [ ] Advanced analytics and learning paths
- [ ] Integration with popular educational APIs
- [ ] Offline mode

## 📄 License

MIT License - Feel free to use and modify

## 🤝 Contributing

To improve this project:
1. Test the features thoroughly
2. Suggest improvements in issues
3. Submit pull requests with enhancements

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Test with valid API key and internet connection

---

**Happy Learning! 🚀**

Built with ❤️ using Streamlit, OpenAI, and Python

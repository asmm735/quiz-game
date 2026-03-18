# Features Documentation

## 1. Ask the Tutor 💡

### Purpose
Get clear, detailed explanations for any topic or question.

### Features
- **Simple Explanations**: Concise overview of the concept
- **Real-World Analogies**: Relatable examples to understand better
- **Key Points**: Summary of important points
- **Follow-Up Questions**: Self-check questions to verify understanding
- **Fun Facts**: Interesting tidbits related to the topic

### How It Works
1. Navigate to "Ask the Tutor"
2. Enter any topic (e.g., "Python exception handling", "photosynthesis")
3. Click "Get Explanation"
4. Read the AI-generated explanation with examples

### Behind the Scenes
- **LLM**: Ollama (neural-chat model)
- **Timeout**: 45 seconds
- **Cached**: Responses are cached to avoid regeneration
- **Format**: JSON with structured fields

## 2. Generate Quiz 📝

### Purpose
Test your understanding with AI-generated multiple-choice questions.

### Features
- **Topic Selection**: Choose any topic to quiz on
- **Difficulty Levels**: Easy, Medium, Hard
- **Custom Count**: 1-10 questions per quiz
- **Instant Feedback**: See if answers are correct immediately
- **Detailed Explanations**: Learn why you got it wrong
- **Concept Correction**: Understand misconceptions

### Quiz Generation Process
1. Select "Generate Quiz"
2. Enter topic (e.g., "recursion in programming")
3. Choose difficulty level
4. Set number of questions
5. Answer each question
6. Get immediate feedback

### Answer Handling
- **Marking**: Each answer is scored immediately
- **Streak Tracking**: Consecutive correct answers build streak
- **Accuracy Calculation**: Your success rate is tracked
- **History**: All quizzes are saved for review

### Behind the Scenes
- **Question Format**: Multiple choice (4 options)
- **Validation**: Questions are validated for quality
- **Timeout**: 120 seconds for generation
- **AI Scoring**: Uses LLM for detailed feedback

## 3. Gamification System 🎮

### Points System
```
Base Points:     10 points per correct answer
Streak Bonus:    +5 points for every 3 correct answers
Perfect Quiz:    1.5x multiplier if all answers correct
```

### Level Progression
```
Level 1: 0-49 points      (Quiz Starter)
Level 2: 50-99 points     (Learning Enthusiast)
Level 3: 100-199 points   (Concept Explorer)
Level 4: 200-399 points   (Knowledge Seeker)
Level 5: 400+ points      (Quiz Champion)
```

### Badges
Users can earn 5 badges by achieving milestones:

| Badge | Requirement | Icon |
|-------|-------------|------|
| Quiz Starter | 50 points | 🥉 |
| Concept Explorer | Learn 10 different topics | 🧭 |
| Concept Master | 200 points | 🥈 |
| Streak Champ | 10-question correct streak | 🔥 |
| Quiz Champion | 500 points | 🥇 |

### Streaks
- **Current Streak**: Consecutive correct answers (resets on wrong)
- **Best Streak**: Highest streak achieved (never resets)
- **Bonus Points**: Every 3 consecutive correct = +5 points

### Accuracy Tracking
- **Quiz Accuracy**: % of answers correct in all quizzes
- **Displayed on**: Progress Dashboard, Sidebar
- **Calculation**: (Total Correct / Total Attempted) × 100

## 4. Progress Dashboard 📊

### Information Displayed
- **Points**: Total points earned
- **Current Level**: Your progression level (1-5)
- **Accuracy %**: Success rate across all quizzes
- **Current Streak**: Consecutive correct answers
- **Best Streak**: Highest streak achieved
- **Badges Earned**: Badge collection display
- **Quiz History**: Recent quizzes with scores
- **Topics Covered**: List of topics studied

### Purpose
- Track your learning journey
- See progress over time
- Identify weak areas
- Celebrate achievements

## 5. Leaderboard 🏆

### Features
- **Global Rankings**: See all users ranked by points
- **User Positions**: Find yourself on the leaderboard
- **Competition**: Motivating list of top performers
- **Full Visibility**: See complete user statistics

### Information
- User rank by points
- Total points for each user
- Current level
- Badge count

## 6. User Authentication & Profiles

### Login/Register
- Create account with username and password
- Password hashing (SHA-256) for security
- Persistent user accounts in data/users.json

### User Data
Each user has:
- Unique username
- Hashed password
- Total points
- Current level
- Badges earned
- Current streak
- Best streak
- Quiz history
- Accuracy percentage
- Topics studied

### Session Management
- One user per session
- Logout button to switch users
- User stats displayed in sidebar

## Performance Metrics

### Response Times
- **Explanation**: 10-45 seconds (depending on model state)
- **Quiz Generation**: 20-120 seconds (5 questions)
- **Cached Response**: <1 second
- **Answer Evaluation**: 10-60 seconds

### Caching Strategy
- Responses are cached by content hash
- Same questions don't regenerate
- Cache persists during session
- Reduces API calls and improves UX

## Technical Details

### LLM Configuration
- **Primary Model**: neural-chat (10-30s responses)
- **Fallback Model**: orca-mini (if neural-chat unavailable)
- **Runtime**: Ollama (local, offline)
- **Auto-detection**: System detects available models

### Data Persistence
- **Format**: JSON (portable, human-readable)
- **Location**: `data/users.json`
- **Auto-save**: Updates after each quiz
- **Backup**: Consider backing up data/users.json

### Validation
- **Quiz Validation**: Checks for quality questions
- **Response Validation**: Rejects placeholder answers
- **Answer Validation**: Verifies answer options match

## Input Limits

- **Topic Length**: No limit (processed as-is)
- **Questions Per Quiz**: 1-10
- **Username Length**: No limit but keep reasonable
- **Password Length**: Minimum recommended 4 characters

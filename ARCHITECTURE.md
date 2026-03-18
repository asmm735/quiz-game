# 🏗️ Architecture & Design

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT UI LAYER                           │
│  (Home | Ask Tutor | Generate Quiz | Progress Dashboard)        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
         ┌──────────────────┼──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
    ┌─────────┐        ┌────────┐        ┌──────────┐
    │ Concept │        │ Quiz   │        │Progress  │
    │ Engine  │        │ Engine │        │ Store    │
    └────┬────┘        └───┬────┘        └──────────┘
         │                 │
         │    ┌────────────┼────────────┐
         │    │            │            │
         ▼    ▼            ▼            ▼
    ┌──────────────────────────────────────────┐
    │         LLM SERVICE LAYER                │
    │  (OpenAI API Interactions)               │
    └──────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────┐
    │      GAMIFICATION ENGINE                 │
    │  (Points, Levels, Streaks, Badges)       │
    └──────────────────────────────────────────┘
         │
         ▼
    ┌──────────────────────────────────────────┐
    │      PERSISTENT STORAGE (JSON)           │
    │  (student_progress.json, quiz_history)   │
    └──────────────────────────────────────────┘
```

---

## Component Details

### 1. LLM Service (`services/llm_service.py`)

**Responsible for:**
- All AI/LLM interactions
- Structured JSON output from LLM
- Prompt engineering for different tasks

**Methods:**

#### `explain_concept(topic, question)`
**Input:**
```
topic: "Recursion"
question: Optional context
```

**Process:**
1. Create teaching-focused prompt
2. Send to OpenAI GPT-3.5
3. Parse JSON response
4. Return structured explanation

**Output:**
```json
{
  "simple_explanation": "...",
  "real_world_analogy": "...",
  "key_points": ["...", "..."],
  "follow_up_question": "...",
  "fun_fact": "..."
}
```

#### `generate_quiz_questions(topic, difficulty, num_questions)`
**Input:**
```
topic: "SQL Joins"
difficulty: "medium"
num_questions: 5
```

**Process:**
1. Create structured quiz prompt
2. Force JSON format in prompt
3. Generate exactly N questions
4. Validate JSON structure
5. Return quiz object

**Output:**
```json
{
  "topic": "SQL Joins",
  "difficulty": "medium",
  "questions": [
    {
      "id": 1,
      "question": "What is a LEFT JOIN?",
      "options": ["A", "B", "C", "D"],
      "correct_answer_index": 0,
      "explanation": "..."
    }
  ]
}
```

#### `evaluate_answer(question, user_answer, correct_answer, options)`
**Purpose:** Evaluate answer quality and provide feedback
**Returns:** Score, explanation, improvement tips

#### `explain_wrong_answer(...)`
**Purpose:** Deep-dive explanation for incorrect answers
**Returns:** Misconception, correct thinking, mnemonics, next steps

---

### 2. Gamification Engine (`services/gamification.py`)

**State Management:**
```
┌─ Points: 0-∞
├─ Streak: 0-N
├─ Topics: Set of explored topics
├─ Badges: []
├─ Level: 1-5
└─ Best Streak: personal record
```

**Points System:**
```
Correct Answer     → +10 points
3-in-a-row Bonus   → +5 points
Each Badge         → Achievement
↓
Level Progression  → 0→49, 50→99, 100→199, 200→399, 400+
```

**Streak Mechanics:**
```
Answer 1 ✓ → Streak: 1
Answer 2 ✓ → Streak: 2
Answer 3 ✓ → Streak: 3 → Bonus +5 points!
Answer 4 ✗ → Streak: 0 (reset)
```

**Badge System:**
```
Badge Name          | Requirement        | Unlock
─────────────────────────────────────────────────
Quiz Starter        | 50 total points    | First milestone
Concept Explorer    | 10 topics studied  | Breadth reward
Concept Master      | 200 total points   | Depth reward
Streak Champ        | 10 correct streak  | Consistency reward
Quiz Champion       | 500 total points   | Excellence reward
```

---

### 3. Progress Store (`services/progress_service.py`)

**File Structure:**

`student_progress.json`
```json
{
  "name": "Student Name",
  "grade": "High School",
  "subject": "General",
  "created_at": "2024-01-01T...",
  "last_updated": "2024-01-15T...",
  "gamification": {
    "points": 150,
    "streak": 3,
    "best_streak": 7,
    "topics_explored": ["Recursion", "APIs"],
    "badges_earned": ["Quiz Starter"],
    "level": 2
  },
  "quizzes": {
    "attempted": 5,
    "accuracy_percentage": 72.5,
    "recent_topics": [...]
  }
}
```

`quiz_history.json`
```json
[
  {
    "topic": "Recursion",
    "difficulty": "easy",
    "questions": 5,
    "correct_answers": 4,
    "score": 80.0,
    "timestamp": "2024-01-15T10:30:00"
  }
]
```

---

### 4. Streamlit UI (`app.py`)

**Session State Management:**
```python
st.session_state:
  ├── llm_service       # Initialized once per session
  ├── progress_store    # Persistent storage handler
  ├── gamification      # Current user's game state
  ├── current_quiz      # Quiz data structure
  ├── quiz_answers      # User's answers dict
  └── show_results      # Display flag
```

**UI Sections:**

#### Home Page
- Feature overview cards
- Quick stats (top right sidebar)
- Learning stats summary

#### Ask the Tutor
- Topic input field
- Explanation display
- Real-world analogy box
- Key points list
- Follow-up question
- Fun fact info box

#### Generate Quiz
- Topic, difficulty, question count inputs
- Quiz generation with spinner
- Question display with radio buttons
- Results section with:
  - Score display
  - Question-by-question review
  - "Explain wrong answer" feature
  - Next action buttons

#### Progress Dashboard
- Total points, level, streak, badges
- Level progress bar
- Quiz statistics
- Badge display
- Recent topics
- Quiz history table

---

## Data Flow Examples

### Example 1: Asking the Tutor

```
1. User Input
   └─ "Explain recursion simply"

2. Concept Engine Processing
   ├─ Create prompt with teaching style
   ├─ Call LLMService.explain_concept()
   └─ Receive JSON:
       ├─ simple_explanation
       ├─ real_world_analogy
       ├─ key_points
       ├─ follow_up_question
       └─ fun_fact

3. UI Display
   ├─ Show explanation in markdown
   ├─ Display analogy in text box
   ├─ List key points as bullets
   ├─ Show question in info box
   └─ Display fun fact

4. Storage
   └─ Add "Recursion" to topics_explored
```

### Example 2: Taking a Quiz

```
1. Quiz Generation
   ├─ User inputs: Topic, Difficulty, Count
   ├─ Call LLMService.generate_quiz_questions()
   ├─ Receive structured questions
   └─ Store in session_state.current_quiz

2. User Answers Questions
   ├─ Radio buttons for each question
   ├─ Track: quiz_answers[f"q_{idx}"] = option_idx
   └─ Submit quiz

3. Score Calculation
   ├─ Compare user answers to correct answers
   ├─ Count correct answers
   ├─ Calculate percentage
   ├─ Award points: correct_count * 10
   └─ Check for streak bonus: +5 if streak % 3 == 0

4. Gamification Update
   ├─ Add points to total
   ├─ Update streak (correct) or reset (wrong)
   ├─ Check for new badges
   ├─ Recalculate level
   └─ Update topics_explored

5. Evaluation and Feedback
   ├─ For wrong answers: Call LLMService.explain_wrong_answer()
   ├─ Show misconception
   ├─ Show correct thinking
   ├─ Show mnemonic trick
   └─ Suggest next steps

6. Storage
   ├─ Save quiz attempt to quiz_history.json
   ├─ Update student_progress.json with:
   │   ├─ New points total
   │   ├─ New level
   │   ├─ Updated streak
   │   └─ Updated badges
   └─ Calculate and update accuracy %
```

### Example 3: Adaptive Difficulty

```
Quiz Score < 40%
    └─ Show: "Try easier difficulty next time!"
       └─ Next quiz auto-sets to Easy

Quiz Score 40-80%
    └─ Show: Encourage taking same difficulty again

Quiz Score > 80%
    └─ Show: "Great job! Try harder difficulty!"
       └─ Next quiz auto-sets to Hard
```

---

## Prompt Engineering Strategy

### Concept Explanation Prompt
**Goal:** Make complex topics understandable to high schoolers

**Key Elements:**
1. Explicit role: "friendly, student-friendly tutor"
2. Language level: "simple terms, avoid jargon"
3. Structure: "analogy, key points, revision bullets"
4. Output format: "Valid JSON only"
5. Temperature: 0.7 (creative but focused)

**Template:**
```
You are a friendly student-friendly teacher. 
Explain [TOPIC] in very simple language, as if explaining to a 14-year-old.

Use examples. Avoid jargon unless absolutely needed.

Respond in valid JSON:
{
    "simple_explanation": "2-3 sentences in plain English",
    "real_world_analogy": "A concrete everyday comparison",
    "key_points": ["Point 1", "Point 2", "Point 3"],
    "follow_up_question": "A question to check understanding",
    "fun_fact": "Something interesting and related"
}
```

### Quiz Generation Prompt
**Goal:** Consistently generate valid, educational MCQs

**Key Constraints:**
1. Exact question count
2. Exactly 4 options per question
3. Exactly 1 correct answer (labeled by index)
4. Clear, unambiguous questions
5. Valid JSON structure
6. Difficulty-appropriate content

**Template:**
```
Generate [N] multiple choice questions about "[TOPIC]" at [DIFFICULTY] level.
Ensure questions are [DIFFICULTY_DESCRIPTION].

Return ONLY valid JSON (no markdown):
{
    "topic": "[TOPIC]",
    "difficulty": "[DIFFICULTY]",
    "questions": [
        {
            "id": 1,
            "question": "Question?",
            "options": ["A", "B", "C", "D"],
            "correct_answer_index": 0,
            "explanation": "Why A is correct"
        }
    ]
}

Constraints:
- Exactly [N] questions
- Exactly 4 options each
- Correct answer index: 0-3
- All options plausible but only 1 correct
```

---

## Performance Considerations

### API Calls
- **Concept explanation**: ~150 tokens average
- **Quiz generation**: ~500 tokens for 5 questions
- **Answer evaluation**: ~100 tokens
- **Cost estimate**: ~$0.01 per interaction

### Storage
- **Per student**: ~5KB (progress) + 1KB per quiz attempt
- **100 students, 100 quizzes each**: ~10MB total

### Latency
- **Concept explanation**: 2-5 seconds
- **Quiz generation**: 3-8 seconds
- **Answer evaluation**: 1-3 seconds
- Users expect this with LLM, show spinners

---

## Extension Points

### Easy to Add:
1. **Custom prompts** in `services/llm_service.py`
2. **New badge conditions** in `services/gamification.py`
3. **Custom leaderboards** in `services/progress_service.py`
4. **New UI sections** in `app.py`

### Moderate Complexity:
1. **Multi-user support** (add user_id to storage)
2. **Different LLM providers** (OpenAI, Gemini, Anthropic)
3. **RAG with study materials** (embed documents, semantic search)
4. **Voice interface** (Whisper + text-to-speech)

### High Complexity:
1. **Spaced repetition algorithm** (calculate review intervals)
2. **Recommendation engine** (suggest next topics)
3. **Vector database** (semantic search in learning materials)
4. **Mobile app** (React Native or Flutter)

---

## Testing Strategy

### Unit Tests (for services)
- `test_llm_service.py`: Mock OpenAI responses
- `test_gamification.py`: Test points, streaks, levels
- `test_progress_service.py`: Test JSON save/load

### Integration Tests
- Full quiz flow: Generate → Answer → Score → Save
- Gamification flow: Points accumulation, level up
- Progress persistence: Save and load correctly

### Manual Testing Checklist
- [ ] Concept explanation returns valid JSON
- [ ] Quiz generates exactly N questions
- [ ] Points calculated correctly
- [ ] Streaks reset on wrong answer
- [ ] Badges unlock at right thresholds
- [ ] Progress persists after restart
- [ ] Adaptive difficulty shows correct messages
- [ ] UI renders on mobile

---

## Security & Privacy

### Current Implementation
- Uses local JSON files (no cloud sync)
- No user authentication
- No data encryption
- Free to deploy locally

### For Production:
1. Add user authentication (Firebase, Auth0)
2. Use encrypted storage (AES-256)
3. Add HTTPS/SSL
4. Implement proper API key management
5. Add rate limiting
6. Add audit logging
7. GDPR compliance for user data

---

This architecture is designed to be:
- **Simple**: Easy to understand and modify
- **Scalable**: Can handle many users locally
- **Extensible**: Easy to add new features
- **Maintainable**: Clear separation of concerns

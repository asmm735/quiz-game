# System Architecture

## Overview

The AI Quiz Tutor is a Streamlit-based learning platform that combines:
- **AI-powered explanations** (via Ollama/neural-chat)
- **Dynamic quiz generation**
- **Gamification system** (points, levels, badges)
- **User management** (authentication, progress tracking)
- **Progress persistence** (JSON storage)

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                   Streamlit Frontend (app.py)               │
│  - User Interface                                           │
│  - Session State Management                                 │
│  - Page Routing                                             │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────────┐  ┌────────────────┐  ┌──────────────┐
   │ LLMService  │  │ UserService    │  │ Gamification │
   │             │  │                │  │ Engine       │
   │ - Explain   │  │ - Auth         │  │              │
   │ - Quiz Gen  │  │ - User Stats   │  │ - Points     │
   │ - Evaluate  │  │ - Persist User │  │ - Levels     │
   └──────┬──────┘  └────────────────┘  │ - Badges     │
          │                              | - Streaks    │
          │                              └──────────────┘
          │
          ▼
   ┌─────────────────────────────────┐
   │  Ollama LLM (neural-chat model) │
   │  Local, Free, Offline           │
   └─────────────────────────────────┘
        │
        ▼
   ┌──────────────────────────────┐
   │   JSON Data Storage          │
   │   - data/users.json          │
   │   - cached responses         │
   └──────────────────────────────┘
```

## Service Layer

### 1. **LLMService** (`services/llm_service.py`)
Handles all LLM interactions:
- Explains concepts with real-world examples
- Generates quiz questions
- Evaluates user answers
- Caches responses to avoid regeneration
- Timeouts: 45s (explanations), 120s (quizzes), 60s (evaluation)

### 2. **UserService** (`services/user_service.py`)
Manages user authentication and tracking:
- User registration and login (SHA-256 hashing)
- Per-user statistics
- Quiz history persistence
- Username is session-based

### 3. **GamificationEngine** (`services/gamification.py`)
Tracks achievements:
- Points calculation
- Level progression
- Badge awards
- Streak management

### 4. **ProgressStore** (`services/progress_service.py`)
Persists user progress:
- Stores quiz history
- Updates user statistics
- JSON-based storage

## Data Flow

### Concept Explanation Flow
```
User Input (Topic) → LLMService.explain_concept() 
→ Ollama (neural-chat) → JSON parsing 
→ Response display
```

### Quiz Generation Flow
```
User Input (Topic, Difficulty) → LLMService.generate_quiz_questions()
→ Ollama (neural-chat) → Validation → Question display
```

### Answer Evaluation Flow
```
User Answer → LLMService.evaluate_answer()
→ Ollama scores → UserService updates points
→ GamificationEngine updates levels/badges
```

## Key Design Decisions

### 1. **Local-First Architecture**
- Uses Ollama (runs locally, completely offline)
- No API keys required
- Zero cloud dependency
- Cost: Free

### 2. **Fast Model Selection**
- primary: neural-chat (10-30s per request)
- fallback: orca-mini (if neural-chat unavailable)
- auto-detection via `/api/tags` endpoint

### 3. **Response Caching**
- MD5 hash of (function_name + arguments)
- Prevents regeneration of same questions
- Improves performance on repeated queries

### 4. **Per-User Tracking**
- UserService maintains user state
- SHA-256 password hashing
- JSON storage ensures portability

### 5. **Validation Layers**
- Quiz validation: checks question structure
- Response validation: rejects placeholder answers
- Answer evaluation: confidence scoring

## Configuration

All settings are centralized in `config/settings.py`:
- LLM timeouts
- Gamification parameters
- Level thresholds
- Badge requirements
- Data directory paths

# Setup Guide

## Prerequisites

- **Python 3.8+**
- **Ollama** (free, local LLM runtime) - [Download here](https://ollama.ai)
- **neural-chat model** in Ollama (or auto-fallback to orca-mini)

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/quiz-game.git
cd quiz-game
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup Ollama

#### Download & Install
- Download Ollama from https://ollama.ai
- Install and run the application

#### Pull the Fast Model
Open terminal and run:
```bash
ollama pull neural-chat
```

Or use a faster alternative:
```bash
ollama pull orca-mini
```

#### Verify Ollama is Running
```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# You should see models listed:
# {"models": [{"name": "neural-chat:latest", ...}, ...]}
```

### 5. Configure Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env if needed (optional - defaults are fine)
# Add your GOOGLE_API_KEY if you want Gemini as fallback
```

### 6. Run the App
```bash
streamlit run app.py
```

App will open at **http://localhost:8501**

## Project Structure

```
quiz-game/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # Project overview
├── config/
│   └── settings.py                # Centralized configuration
├── services/
│   ├── __init__.py
│   ├── llm_service.py            # LLM interactions (explanations, quizzes)
│   ├── user_service.py           # User auth and statistics
│   ├── gamification.py           # Points, levels, badges, streaks
│   └── progress_service.py       # Progress persistence
├── utils/
│   ├── prompts.py                # LLM prompt templates
│   └── constants.py              # Constants (if needed)
├── data/
│   └── users.json                # User data (auto-created)
├── docs/
│   ├── ARCHITECTURE.md           # System design
│   ├── SETUP.md                  # This file
│   └── FEATURES.md               # Feature documentation
└── venv/                          # Virtual environment (ignored in git)
```

## Troubleshooting

### Issue: "Ollama not responding"
**Solution:** 
1. Ensure Ollama is installed and running
2. Check firewall isn't blocking port 11434
3. Run: `ollama serve` in terminal

### Issue: "Model not found"
**Solution:**
1. Pull the model: `ollama pull neural-chat`
2. Check available models: `ollama list`
3. Restart Ollama

### Issue: Responses are slow (>45 seconds)
**Solution:**
1. Pull faster model: `ollama pull orca-mini`
2. Check your GPU is being used
3. Reduce timeouts in `config/settings.py` if needed

### Issue: "Port 8501 already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

## Running Tests

While test files have been removed, you can test manually by:
1. Starting the app: `streamlit run app.py`
2. Login/Register with a test account
3. Try "Ask the Tutor" section
4. Generate and take a quiz
5. Check Progress Dashboard for updated points

## Performance Notes

- **Cold start**: First explanation (~45s) - model initializing
- **Warm responses**: Subsequent requests (~10-30s)
- **Cache hits**: ~1s if same question asked before
- **Total quiz time**: 2-3 minutes for 5 questions

## Support

For issues or questions:
1. Check ARCHITECTURE.md for system design
2. Review config/settings.py for customization
3. Check app.py for implementation details

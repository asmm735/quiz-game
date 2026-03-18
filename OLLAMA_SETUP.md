# Ollama Setup Guide

## Step 1: Download Ollama
1. Go to https://ollama.ai
2. Click "Download"
3. Download the Windows version
4. Install it (like any other app)

## Step 2: Pull the Model
After installing, open PowerShell and run:
```powershell
ollama pull mistral
```

This downloads Mistral 7B (~4GB, takes a few minutes).

## Step 3: Start Ollama
Ollama runs automatically as a background service. You should see it in the system tray.

To check if it's running:
```powershell
curl http://localhost:11434/api/tags
```

You should see a JSON response with the models.

## Step 4: Restart the App
```powershell
.\venv\Scripts\streamlit run app.py
```

The app will connect to Ollama automatically!

## Troubleshooting

**"Cannot connect to Ollama"**
- Make sure Ollama is running
- Check the system tray for Ollama icon
- Or run from command line: `ollama serve`

**Model not found**
- Pull mistral: `ollama pull mistral`
- Or use another model: `ollama pull neural-chat` (smaller, faster)

**Very slow responses**
- This is normal for first run (model is loading)
- Mistral is optimized for local (not as fast as cloud APIs but completely free!)

# TruthLens — Fake News Detector

An AI-powered fake news detection website built with Python (Flask) and HTML.

## How it works
1. User pastes a news headline or article
2. Flask backend sends it to Groq AI (LLaMA model)
3. AI analyzes credibility and returns a verdict

## Tech Stack
- Frontend: HTML, CSS, JavaScript
- Backend: Python, Flask
- AI Model: LLaMA 3.3 via Groq API

## How to run
1. Install dependencies:
   pip install flask flask-cors groq python-dotenv
2. Add your Groq API key in a .env file:
   GROQ_API_KEY=your_key_here
3. Run the backend:
   python app.py
4. Open http://127.0.0.1:5000 in your browser
```

---

### 4. Create a `.gitignore` file
Create a file called `.gitignore` in your DSP folder:
```
.env
__pycache__/
*.pyc
```

---

### 5. Your final folder should look like this
```
DSP/
├── app.py
├── index.html
├── README.md
├── .env          ← never uploaded to GitHub
└── .gitignore
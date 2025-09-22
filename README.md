# 🧠 AI Task Planner

An interactive **Streamlit app** that generates structured daily plans for any goal (travel itineraries, workout routines, study schedules, etc.).  
Plans are stored in a local database so you can view them later.

---

## ⚙️ How It Works

1. Enter a **goal** (e.g., “Plan a 2-day vegetarian food tour in Hyderabad” or “Make a 3-day beginner workout plan”).
2. The app uses an **AI planning agent** to generate a structured plan.
3. Plans are displayed with **tasks, places, and weather context** (if relevant).
4. Each plan is **saved in SQLite** and can be revisited later.

### 📝 Simple Diagram

```
[ User Goal ] 
     │
     ▼
[ AI Planner Agent ] → Calls Web Search API (optional for weather/places)
     │
     ▼
[ Structured Plan JSON ]
     │
     ▼
[ Streamlit UI ]  ↔  [ SQLite DB (History) ]
```

---

## 🚀 Setup & Run Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/task-planner.git
cd task-planner
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your API keys  
- Create a `.env` file in the project root:  
```env
OPENAI_API_KEY=your_openai_key_here
WEBSEARCH_API_KEY=your_websearch_api_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser 🎉



## 📜 Disclosure of AI Assistance

This project was built with assistance from **AI (OpenAI’s GPT-5 via ChatGPT)** for:
- Writing parts of the `app.py` and planner agent logic.  
- Debugging errors (`NoneType` handling for places/weather).  
- Drafting this README.

---

## 🎥 Demo Recording

Click here to view the demo recording: [video.mp4](video.mp4)


All code was reviewed, tested, and adapted manually.

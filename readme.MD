# 🧞 Course Genie

**Course Genie** is an **AI-powered course recommender** that helps learners find the best courses based on their interests, goals, and skill level.  
It uses the OpenAI API to generate intelligent course suggestions and personalized learning paths.

---

## 🚀 Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

---

## 🔑 OpenAI API Key Setup

To enable AI recommendations, set up your OpenAI API key:

1. Get your key from [OpenAI](https://platform.openai.com/account/api-keys)
2. Create a `.env` file in the `backend` directory
3. Add:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
4. Restart your Flask server after saving.

---

> ✨ _Course Genie — your AI companion for personalized course discovery and recommendation._

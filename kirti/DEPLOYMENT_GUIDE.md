# ☁️ Desh Bhagat University — Cloud Deployment Guide (Render / Railway)

This guide walks you step-by-step through deploying your **AI Kiosk Receptionist** to the cloud (Render or Railway) so anyone can access it over the web!

---

## 🌟 Recommended Cloud Provider: **Render** (Free & Easy)

### Step 1: Push your code to GitHub
1. Create a GitHub repository (e.g., `dbu-ai-kiosk`).
2. Push your project files to GitHub.

---

### Step 2: Deploy on Render
1. Go to [render.com](https://render.com) and log in.
2. Click **New +** → **Web Service**.
3. Connect your GitHub repository.
4. Fill in the deployment details:
   - **Name**: `dbu-ai-kiosk`
   - **Environment**: `Python 3`
   - **Region**: `Singapore` (or closest to India)
   - **Build Command**: `pip install -r kirti/requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT kirti.cat_ui_server:app`

---

### Step 3: Add your Environment Variables (API Keys)
In Render Dashboard under **Environment Variables**, add:
- `GEMINI_API_KEY` = *(Your Gemini API key)*
- `GROQ_API_KEY` = *(Your Groq API key)*
- `TTS_API_KEY` = *(Your TTS API key)*

Click **Deploy Web Service**! 🚀

---

## 🌐 Visiting your Live Kiosk

Once deployed, Render gives you a public URL (e.g., `https://dbu-ai-kiosk.onrender.com`).

- **Normal URL**: `https://dbu-ai-kiosk.onrender.com/`
- **Force Active Kiosk Mode**: `https://dbu-ai-kiosk.onrender.com/?bypass=true`

---

## 📁 Files Included for Cloud Deployment:
- **`Procfile`**: Defines production Gunicorn start command.
- **`render.yaml`**: Pre-configured Render deployment configuration.
- **`kirti/requirements.txt`**: Complete Python package manifest (includes `gunicorn` + `python-dotenv`).

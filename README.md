# 🤖 Interactive Campus Robot Assistant

A cloud-deployed Retrieval-Augmented Generation (RAG) web assistant designed to answer student queries about campus facilities, hostel timings, library rules, bus schedules, and placements.

## 🌐 Live Demo
* **Frontend Web App (Streamlit):** [Launch Campus Robot Assistant](https://streamlit.app)
* **Backend API (Render):** `https://onrender.com`

## 🏗️ System Architecture
* **Frontend (`app.py`):** Built with **Streamlit** featuring a custom robotics-inspired dark UI, quick-topic preset buttons, and conversation history logs.
* **Backend (`cloud_api.py`):** Built with **FastAPI** and hosted on **Render**.
* **Retrieval Engine:** Uses **Scikit-Learn TF-IDF Vectorization & Cosine Similarity** over `college_guide.txt` to retrieve the most relevant campus guidelines.
* **LLM Inference:** Powered by **Groq Cloud API** (`openai/gpt-oss-20b`) for fast, grounded responses without requiring local GPU hardware.

## 📂 Project Structure
```text
├── app.py               # Streamlit frontend interface
├── cloud_api.py         # FastAPI + TF-IDF + Groq RAG backend
├── college_guide.txt    # Campus knowledge base document
└── requirements.txt     # Python dependencies for frontend & backend
```

## 🚀 Running Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd campus-robot-cloud
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Streamlit frontend:
   ```bash
   streamlit run app.py
   ```

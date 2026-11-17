import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title="Campus AI Robot Cloud API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    question: str

def load_chunks():
    if not os.path.exists("college_guide.txt"):
        return ["Campus information database is currently empty."]
    with open("college_guide.txt", "r", encoding="utf-8") as f:
        text = f.read()
    return [b.strip() for b in text.split("\n\n") if b.strip()]

CHUNKS = load_chunks()
VECTORIZER = TfidfVectorizer(stop_words="english")
CHUNK_VECTORS = VECTORIZER.fit_transform(CHUNKS)

def retrieve_context(question: str, top_k: int = 4) -> str:
    q_vec = VECTORIZER.transform([question])
    scores = cosine_similarity(q_vec, CHUNK_VECTORS).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    return "\n\n".join(CHUNKS[i] for i in top_indices if scores[i] > 0) or "\n\n".join(CHUNKS[:2])

@app.get("/")
def health_check():
    return {"status": "online", "model": "llama-3.1-8b-instant", "chunks": len(CHUNKS)}

@app.post("/ask")
def ask_robot(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="GROQ_API_KEY is missing on Render.")

    context = retrieve_context(req.question, top_k=4)
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an intelligent AI robot assistant on a college campus. "
        "Answer the student's question accurately using ONLY the provided context. "
        "If the student asks multiple questions, answer EVERY part clearly. "
        "Keep answers concise and natural for mobile voice playback without markdown symbols. "
        "If the information is missing, state clearly that you do not have that information in your database logs."
    )

    chat_completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0.1,
        max_tokens=300,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {req.question}"}
        ],
    )

    clean_answer = chat_completion.choices[0].message.content.replace("*", "").replace("#", "")
    return {"question": req.question, "answer": clean_answer}

from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import json
import random
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from fuzzywuzzy import process

# 載入環境變數
load_dotenv()

app = FastAPI()

# CORS 設定，允許所有前端請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# 設定 OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 📂 **載入 FAQ JSON**
faq_data = [
    {"question": "How do I reset my password?", "answer": "Go to Settings -> Security -> Reset Password."},
    {"question": "My VPN is not working, what should I do?", "answer": "Restart your computer and try again."},
    {"question": "How do I request a new laptop?", "answer": "Submit an IT request ticket via the IT Support Portal."}
]

# 儲存使用者對話紀錄
user_sessions = {}

# 儲存報修單
tickets = []

# 📌 **模糊匹配 FAQ 問題**
def check_faq(question):
    questions = [faq["question"] for faq in faq_data]
    best_match, score = process.extractOne(question, questions)
    if score > 70:
        return next(faq["answer"] for faq in faq_data if faq["question"] == best_match)
    return None

# 🎯 **聊天 API**
class ChatRequest(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
async def chat(query: ChatRequest):
    user_id = query.user_id
    question = query.message

    # 建立使用者對話紀錄
    if user_id not in user_sessions:
        user_sessions[user_id] = []

    # 1️⃣ **先查詢 FAQ**
    faq_answer = check_faq(question)
    if faq_answer:
        return {"response": faq_answer, "suggest_ticket": False}

    # 2️⃣ **如果 FAQ 沒有答案，使用 OpenAI 回答**
    messages = [{"role": "system", "content": "You are an IT support assistant."}]
    messages += user_sessions[user_id][-5:]  # 只保留最近 5 則對話

    messages.append({"role": "user", "content": question})

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    bot_response = response['choices'][0]['message']['content']

    # 儲存對話
    user_sessions[user_id].append({"role": "user", "content": question})
    user_sessions[user_id].append({"role": "assistant", "content": bot_response})

    # 3️⃣ **如果 AI 回答不夠明確，提供報修建議**
    suggest_ticket = "contact IT support" in bot_response.lower() or "unable to help" in bot_response.lower()

    return {"response": bot_response, "suggest_ticket": suggest_ticket}

# 🎟️ **IT 報修 API**
class TicketRequest(BaseModel):
    user_id: str
    issue: str

@app.post("/ticket")
async def create_ticket(ticket: TicketRequest):
    ticket_id = random.randint(1000, 9999)
    new_ticket = {
        "ticket_id": ticket_id,
        "user_id": ticket.user_id,
        "issue": ticket.issue,
        "status": "submitted"
    }
    tickets.append(new_ticket)
    return new_ticket

@app.get("/tickets")
async def get_tickets():
    return tickets

# **啟動應用**
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))  # 預設為 8000
    uvicorn.run(app, host="0.0.0.0", port=port)

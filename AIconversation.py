from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from generate import generate_reply
from messagefunctions import add_conversation, get_messages_by_conversation, save_message
import uvicorn

app = FastAPI()

# 🔥 Fix CORS so React can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change to specific URL later for security)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Add a default root endpoint
@app.get("/")
def read_root():
    return {"status": "FastAPI Chatbot API is running 🚀"}

@app.post("/chat/")
async def chat_with_ai(request_data: dict):
    """Handles chat messages from React and returns AI responses."""
    try:
        user_id = request_data.get("user_id")
        conversation_id = request_data.get("conversation_id")
        user_message = request_data.get("user_message")

        if not user_message:
            raise HTTPException(status_code=400, detail="User message is required")

        # 🔥 Fetch last 'N' messages for AI context (do NOT save them)
        conversation_history = get_messages_by_conversation(conversation_id, limit=10)

        # 🔥 Format for AI but do not save
        chat_history = "\n".join([
            f"User: {msg.get('user_message', '')}\nAI: {msg.get('assistant_message', '')}" 
            for msg in conversation_history if isinstance(msg, dict)
        ])

        AI_behaviour="You are a helpful AI."
        # 🔥 Generate AI Response
        ai_reply = generate_reply(conversation_id, f"{chat_history}\nUser: {user_message}", AI_behaviour, 5)

        if not ai_reply:  
            ai_reply = "Sorry, I couldn't generate a response. Please try again."

        # 🔥 Save only after AI responds
        save_message(conversation_id, user_message, ai_reply)

        return {"user_message": user_message, "assistant_message": ai_reply}

    except Exception as e:
        print(f"❌ ERROR in FastAPI: {e}")
        return {"message": f"Internal Server Error: {str(e)}"}

# Run FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

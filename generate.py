import os
from openai import OpenAI
from messagefunctions import get_messages_by_conversation  # 🚀 Removed save_message from here

# Load API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY environment variable is not set!")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

def generate_reply(conversation_id, user_message, ai_role, past_messages_number=5):
    """Generates a reply based on past conversation with a specific conversation ID."""
    print(f"DEBUG: generate_reply called with conversation_id={conversation_id}")

    # 🔥 Fetch only the last 'N' messages from Firestore for AI context
    past_messages = get_messages_by_conversation(conversation_id, past_messages_number)

    # ✅ Format conversation history for AI (but do NOT save it)
    message_history = [{"role": "system", "content": ai_role}]
    for msg in past_messages:
        message_history.append({"role": "user", "content": msg.get("user_message", "").strip()})
        message_history.append({"role": "assistant", "content": msg.get("assistant_message", "").strip()})

    # Add the new user message to context
    message_history.append({"role": "user", "content": user_message.strip()})

    print("\nWaiting for AI response...")

    try:
        # Generate AI response
        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=message_history
        )

        # Extract the response safely
        if completion and completion.choices and len(completion.choices) > 0:
            new_message = completion.choices[0].message.content.strip()
        else:
            new_message = "I'm not sure how to respond to that."

        print(f"DEBUG: AI Response received: {new_message}")  # Debug print

        return new_message  # 🚀 Only return the response, do NOT save it here

    except Exception as e:
        print(f"Error generating AI response: {e}")
        return "I'm having trouble responding right now. Try again later."

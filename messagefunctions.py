from firebaseconfig import db
from firebase_admin import firestore
from datetime import datetime

def save_message(conversation_id, user_text, assistant_text):
    """Saves user + assistant message ONLY after AI responds."""
    messages_ref = db.collection("conversations").document(str(conversation_id)).collection("messages")

    # ✅ Check if identical message exists before saving
    existing_messages = messages_ref.where("user_message", "==", user_text).where("assistant_message", "==", assistant_text).limit(1).stream()
    
    if any(existing_messages):  
        print("⚠️ Duplicate message detected. Skipping save.")
        return

    # ✅ Save message only after AI responds
    message_data = {
        "user_message": user_text.strip(),
        "assistant_message": assistant_text.strip(),
        "timestamp": datetime.utcnow(),
    }
    messages_ref.add(message_data)
    print(f"✅ Message saved for conversation {conversation_id}!")





def get_messages_by_conversation(conversation_id, limit=10):
    """Fetch the latest 'limit' messages from Firestore for a given conversation."""
    messages_ref = (
        db.collection("conversations")
        .document(str(conversation_id))
        .collection("messages")
        .order_by("timestamp", direction=firestore.Query.DESCENDING)  # ✅ Fix: Fetch latest messages first
        .limit(limit)
    )
    messages = messages_ref.stream()

    # ✅ Return a properly formatted list of dictionaries (NOT tuples)
    return [msg.to_dict() for msg in messages if isinstance(msg.to_dict(), dict)][::-1]  # ✅ Reverse to chronological order


def add_conversation(description):
    """Creates a new conversation with a numeric ID instead of Firestore's random ID."""
    conversations_ref = db.collection("conversations")

    # Get the last numeric conversation ID
    last_conversations = conversations_ref.order_by("created_at", direction=firestore.Query.DESCENDING).limit(1).stream()
    last_id = 0

    for conv in last_conversations:
        if conv.id.isdigit():  # ✅ Only convert if ID is numeric
            last_id = int(conv.id)

    new_id = str(last_id + 1)  # Generate next numeric ID as a string

    # Save new conversation with the numeric ID
    conversations_ref.document(new_id).set({
        "conversation_description": description,
        "created_at": datetime.utcnow()
    })

    print(f"✅ New conversation created: ID {new_id}, Description: {description}")
    return new_id


def list_conversations():
    """Lists all conversations in Firestore."""
    conversations = db.collection("conversations").stream()
    conversation_list = [(conv.id, conv.to_dict()["conversation_description"]) for conv in conversations]

    if not conversation_list:
        print("⚠️ No conversations found.")
        return []

    print("\n📜 Available Conversations:")
    for conv_id, conv_desc in conversation_list:
        print(f"[{conv_id}] - {conv_desc}")

    return conversation_list

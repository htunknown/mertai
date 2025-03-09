import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials from environment variable
firebase_json = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_json:
    raise ValueError("❌ FIREBASE_CREDENTIALS environment variable is not set!")

try:
    cred_dict = json.loads(firebase_json)  # Convert string back to JSON
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("🔥 Firebase Firestore is connected!")
except Exception as e:
    print(f"❌ Error initializing Firebase: {e}")

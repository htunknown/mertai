import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials (replace with your actual file path)
cred = credentials.Certificate("chat-with-mert-firebase-adminsdk-fbsvc-9733b19087.json")

# Initialize Firebase
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

print("🔥 Firebase Firestore is connected!")

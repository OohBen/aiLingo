from flask import Flask, jsonify, request

app = Flask(__name__)

# Hardcoded example data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com", "password": "password123", "profile_pic": None, "date_joined": "2023-04-15", "is_premium": False, "home_language": 1, "is_active": True, "is_staff": False},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "password": "password456", "profile_pic": None, "date_joined": "2023-04-16", "is_premium": True, "home_language": 2, "is_active": True, "is_staff": False},
]

languages = [
    {"id": 1, "name": "English", "code": "en"},
    {"id": 2, "name": "Spanish", "code": "es"},
]

lessons = [
    {"id": 1, "language": 1, "title": "Introduction to English", "content": "Welcome to the English language course!"},
    {"id": 2, "language": 2, "title": "Introduction to Spanish", "content": "Welcome to the Spanish language course!"},
]

quizzes = [
    {"id": 1, "language": 1, "title": "English Quiz 1", "duration": 30, "passing_score": 80},
    {"id": 2, "language": 2, "title": "Spanish Quiz 1", "duration": 25, "passing_score": 75},
]

questions = [
    {"id": 1, "quiz": 1, "text": "What is the capital of England?", "choices": ["London", "Paris", "Berlin", "Madrid"], "answer": 1, "explanations": ["London is the capital of England."], "worth": 5},
    {"id": 2, "quiz": 2, "text": "What is the Spanish word for 'hello'?", "choices": ["Hola", "Adios", "Gracias", "Por favor"], "answer": 1, "explanations": ["'Hola' means 'hello' in Spanish."], "worth": 3},
]

attempts = [
    {"id": 1, "user": 1, "quiz": 1, "score": 90, "date": "2023-04-17"},
    {"id": 2, "user": 2, "quiz": 2, "score": 80, "date": "2023-04-18"},
]

conversations = [
    {"id": 1, "user": 1, "language": 1, "title": "English Conversation 1", "created_at": "2023-04-17"},
    {"id": 2, "user": 2, "language": 2, "title": "Spanish Conversation 1", "created_at": "2023-04-18"},
]

messages = [
    {"id": 1, "conversation": 1, "sender": "user", "content": "Hello, how are you?", "timestamp": "2023-04-17 10:00:00"},
    {"id": 2, "conversation": 1, "sender": "bot", "content": "I'm doing well, thank you! How can I assist you today?", "timestamp": "2023-04-17 10:01:00"},
    {"id": 3, "conversation": 2, "sender": "user", "content": "Hola, ¿cómo estás?", "timestamp": "2023-04-18 11:00:00"},
    {"id": 4, "conversation": 2, "sender": "bot", "content": "Estoy bien, ¡gracias! ¿En qué puedo ayudarte hoy?", "timestamp": "2023-04-18 11:01:00"},
]

analytics = [
    {"id": 1, "user": 1, "language_progress": {"English": 75, "Spanish": 60}, "quiz_analytics": {"English": [90, 85], "Spanish": [80, 75]}, "chat_analytics": {"English": 10, "Spanish": 5}},
    {"id": 2, "user": 2, "language_progress": {"English": 80, "Spanish": 70}, "quiz_analytics": {"English": [95, 90], "Spanish": [85, 80]}, "chat_analytics": {"English": 8, "Spanish": 12}},
]

# User endpoints
@app.route("/api/users/register/", methods=["POST"])
def register_user():
    user_data = request.json
    user = {
        "id": len(users) + 1,
        "name": user_data["name"],
        "email": user_data["email"],
        "password": user_data["password"],
        "profile_pic": None,
        "date_joined": "2023-04-20",
        "is_premium": False,
        "home_language": user_data["home_language"],
        "is_active": True,
        "is_staff": False,
    }
    users.append(user)
    return jsonify({"user": user, "access": "dummy_access_token", "refresh": "dummy_refresh_token"})

@app.route("/api/users/login/", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
    user = next((u for u in users if u["email"] == email and u["password"] == password), None)
    if user:
        return jsonify({"user": user, "access": "dummy_access_token", "refresh": "dummy_refresh_token"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/api/users/profile/", methods=["GET"])
def get_user_profile():
    user_id = 1  # Hardcoded user ID for simplicity
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/api/users/refresh-token/", methods=["POST"])
def refresh_token():
    return jsonify({"access": "dummy_access_token"})

# Language endpoints
@app.route("/api/languages/", methods=["GET"])
def get_languages():
    return jsonify(languages)

@app.route("/api/languages/<int:language_id>/", methods=["GET"])
def get_language(language_id):
    language = next((l for l in languages if l["id"] == language_id), None)
    if language:
        return jsonify(language)
    else:
        return jsonify({"error": "Language not found"}), 404

# Lesson endpoints
@app.route("/api/lessons/", methods=["GET"])
def get_lessons():
    return jsonify(lessons)

# Quiz endpoints
@app.route("/api/quizzes/", methods=["GET"])
def get_quizzes():
    return jsonify(quizzes)

@app.route("/api/quizzes/<int:quiz_id>/", methods=["GET"])
def get_quiz(quiz_id):
    quiz = next((q for q in quizzes if q["id"] == quiz_id), None)
    if quiz:
        return jsonify(quiz)
    else:
        return jsonify({"error": "Quiz not found"}), 404

@app.route("/api/quizzes/<int:quiz_id>/questions/", methods=["GET"])
def get_quiz_questions(quiz_id):
    quiz_questions = [q for q in questions if q["quiz"] == quiz_id]
    return jsonify(quiz_questions)

@app.route("/api/quizzes/attempt/", methods=["POST"])
def attempt_quiz():
    attempt_data = request.json
    attempt = {
        "id": len(attempts) + 1,
        "user": attempt_data["user"],
        "quiz": attempt_data["quiz"],
        "score": attempt_data["score"],
        "date": "2023-04-20",
    }
    attempts.append(attempt)
    return jsonify(attempt)

# Conversation endpoints
@app.route("/api/chat/conversations/", methods=["GET"])
def get_conversations():
    user_conversations = [c for c in conversations if c["user"] == 1]  # Hardcoded user ID for simplicity
    return jsonify(user_conversations)

@app.route("/api/chat/conversations/", methods=["POST"])
def create_conversation():
    conversation_data = request.json
    conversation = {
        "id": len(conversations) + 1,
        "user": 1,  # Hardcoded user ID for simplicity
        "language": conversation_data["language"],
        "title": conversation_data["title"],
        "created_at": "2023-04-20",
    }
    conversations.append(conversation)
    return jsonify(conversation)

@app.route("/api/chat/conversations/<int:conversation_id>/messages/", methods=["GET"])
def get_conversation_messages(conversation_id):
    conversation_messages = [m for m in messages if m["conversation"] == conversation_id]
    return jsonify(conversation_messages)

@app.route("/api/chat/conversations/<int:conversation_id>/messages/", methods=["POST"])
def create_message(conversation_id):
    message_data = request.json
    message = {
        "id": len(messages) + 1,
        "conversation": conversation_id,
        "sender": message_data["sender"],
        "content": message_data["content"],
        "timestamp": "2023-04-20 12:00:00",
    }
    messages.append(message)
    return jsonify(message)

# Analytics endpoints
@app.route("/api/analytics/user-analytics/", methods=["GET"])
def get_user_analytics():
    user_id = 1  # Hardcoded user ID for simplicity
    user_analytics = next((a for a in analytics if a["user"] == user_id), None)
    if user_analytics:
        return jsonify(user_analytics)
    else:
        return jsonify({"error": "Analytics not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
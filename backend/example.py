from flask import Flask, jsonify

app = Flask(__name__)

# Languages Models
languages = [
    {
        "id": 1,
        "name": "English",
        "code": "en"
    },
    {
        "id": 2,
        "name": "Spanish",
        "code": "es"
    },
    {
        "id": 3,
        "name": "French",
        "code": "fr"
    }
]

lessons = [
    {
        "id": 1,
        "language": 1,
        "title": "English Grammar Basics",
        "content": "This is the content for the English Grammar Basics lesson.",
        "tags": ["beginner", "english", "grammar"]
    },
    {
        "id": 2,
        "language": 2,
        "title": "Spanish Vocabulary",
        "content": "This is the content for the Spanish Vocabulary lesson.",
        "tags": ["beginner", "spanish", "vocabulary"]
    },
    {
        "id": 3,
        "language": 3,
        "title": "French Pronunciation",
        "content": "This is the content for the French Pronunciation lesson.",
        "tags": ["intermediate", "french", "pronunciation"]
    }
]

quizzes = [
    {
        "id": 1,
        "language": 1,
        "title": "English Grammar Quiz",
        "questions": [1, 2],
        "duration": 30,
        "passing_score": 80
    },
    {
        "id": 2,
        "language": 2,
        "title": "Spanish Vocabulary Quiz",
        "questions": [3, 4],
        "duration": 45,
        "passing_score": 75
    },
    {
        "id": 3,
        "language": 3,
        "title": "French Pronunciation Quiz",
        "questions": [5, 6],
        "duration": 20,
        "passing_score": 70
    }
]

questions = [
    {
        "id": 1,
        "text": "What is the correct way to use the verb 'to be' in the present tense?",
        "choices": ["I is", "I am", "I are", "I be"],
        "answer": 1
    },
    {
        "id": 2,
        "text": "What is the plural form of 'child'?",
        "choices": ["childs", "childrens", "children", "childres"],
        "answer": 2
    },
    {
        "id": 3,
        "text": "What is the Spanish word for 'book'?",
        "choices": ["libro", "papel", "cuaderno", "lapiz"],
        "answer": 0
    },
    {
        "id": 4,
        "text": "How do you say 'Hello' in Spanish?",
        "choices": ["Hola", "Adios", "Gracias", "Buenos dias"],
        "answer": 0
    },
    {
        "id": 5,
        "text": "How is the word 'bonjour' pronounced in French?",
        "choices": ["bon-jour", "bon-zhoor", "bon-joor", "bon-jure"],
        "answer": 1
    },
    {
        "id": 6,
        "text": "What is the correct pronunciation of the French word 'merci'?",
        "choices": ["mer-see", "mer-see", "mer-chi", "mer-key"],
        "answer": 1
    }
]

# Routes
@app.route('/languages', methods=['GET'])
def get_languages():
    return jsonify(languages)

@app.route('/languages/<int:language_id>', methods=['GET'])
def get_language(language_id):
    language = next((l for l in languages if l['id'] == language_id), None)
    if language:
        return jsonify(language)
    else:
        return jsonify({"error": "Language not found"}), 404

@app.route('/languages/<int:language_id>/lessons', methods=['GET'])
def get_language_lessons(language_id):
    lessons_for_language = [l for l in lessons if l['language'] == language_id]
    if lessons_for_language:
        return jsonify(lessons_for_language)
    else:
        return jsonify({"error": "No lessons found for this language"}), 404

@app.route('/lessons/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    lesson = next((l for l in lessons if l['id'] == lesson_id), None)
    if lesson:
        return jsonify(lesson)
    else:
        return jsonify({"error": "Lesson not found"}), 404

@app.route('/languages/<int:language_id>/quizzes', methods=['GET'])
def get_language_quizzes(language_id):
    quizzes_for_language = [q for q in quizzes if q['language'] == language_id]
    if quizzes_for_language:
        return jsonify(quizzes_for_language)
    else:
        return jsonify({"error": "No quizzes found for this language"}), 404

@app.route('/quizzes/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    quiz = next((q for q in quizzes if q['id'] == quiz_id), None)
    if quiz:
        quiz_questions = [q for q in questions if q['id'] in quiz['questions']]
        quiz['questions'] = quiz_questions
        return jsonify(quiz)
    else:
        return jsonify({"error": "Quiz not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
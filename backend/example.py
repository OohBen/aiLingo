from flask import Flask, jsonify
"""
GET /languages: Get a list of all languages
GET /languages/<int:language_id>: Get details of a specific language
GET /languages/<int:language_id>/lessons: Get a list of lessons for a specific language
GET /languages/<int:language_id>/quizzes: Get a list of quizzes for a specific language
GET /quizzes/<int:quiz_id>: Get details of a specific quiz, including its questions
"""
app = Flask(__name__)

# Languages Models
languages = [
    {
        "id": 1,
        "name": "Python",
        "code": "py"
    },
    {
        "id": 2,
        "name": "JavaScript",
        "code": "js"
    }
]

lessons = [
    {
        "id": 1,
        "language": 1,
        "title": "Introduction to Python",
        "content": "This is the content for the Python intro lesson.",
        "tags": ["beginner", "python"]
    },
    {
        "id": 2,
        "language": 2,
        "title": "JavaScript Basics",
        "content": "This is the content for the JavaScript basics lesson.",
        "tags": ["beginner", "javascript"]
    }
]

quizzes = [
    {
        "id": 1,
        "language": 1,
        "title": "Python Quiz 1",
        "questions": [1, 2],
        "duration": 30,
        "passing_score": 80
    },
    {
        "id": 2,
        "language": 2,
        "title": "JavaScript Quiz 1",
        "questions": [3, 4],
        "duration": 45,
        "passing_score": 75
    }
]

questions = [
    {
        "id": 1,
        "text": "What is the output of print(2 + 2)?",
        "choices": ["2", "4", "6", "8"],
        "answer": 2
    },
    {
        "id": 2,
        "text": "What is the result of 5 * 3?",
        "choices": ["8", "12", "15", "18"],
        "answer": 3
    },
    {
        "id": 3,
        "text": "Which operator is used to assign a value to a variable?",
        "choices": ["+", "-", "=", "*"],
        "answer": 2
    },
    {
        "id": 4,
        "text": "What is the correct way to write a comment in JavaScript?",
        "choices": ["/* Comment */", "// Comment", "# Comment", "{ Comment }"],
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
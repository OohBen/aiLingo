from datetime import datetime
from typing import List
from ninja import Schema

class QuestionSchema(Schema):
    id: int
    quiz_id: int
    text: str
    choices: List[str]
    answer: int
    explanations: List[str] = None
    worth: int = 1

class QuizSchema(Schema):
    id: int
    user_id: int
    language_id: int
    title: str
    duration: int
    passing_score: int
    questions: List[QuestionSchema] = []

class AttemptSchema(Schema):
    id: int
    user_id: int
    quiz_id: int
    score: int
    date: datetime
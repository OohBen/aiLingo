import json
from typing import List
from rest_framework import status
from ninja import Router
from ninja.responses import codes_4xx
from backend.aiLingoNew.users.api import AuthBearer
from languages.models import Language
from quizzes.models import Question, Quiz
from quizzes.schemas import QuestionSchema
from .models import Conversation, Message
from .schemas import ConversationSchema, MessageSchema
from django.conf import settings
import google.generativeai as genai
from analytics.models import UserAnalytics

router = Router()

@router.post("/conversations", response={201: ConversationSchema, codes_4xx: None}, auth=AuthBearer())
async def create_conversation(request, language_id: str, title: str):
    language = await Language.objects.aget(id=language_id)
    conversation = await Conversation.objects.acreate(user=request.auth, language=language, title=title)
    return 201, conversation

@router.get("/conversations", response=List[ConversationSchema], auth=AuthBearer())
async def list_conversations(request):
    conversations = await Conversation.objects.filter(user=request.auth).all()
    return conversations

@router.get("/conversations/{conversation_id}/messages", response=List[MessageSchema], auth=AuthBearer())
async def list_messages(request, conversation_id: str):
    conversation = await Conversation.objects.aget(id=conversation_id, user=request.auth)
    messages = await Message.objects.filter(conversation=conversation).all()
    return messages

@router.post("/conversations/{conversation_id}/messages", response={201: MessageSchema, codes_4xx: None}, auth=AuthBearer())
async def send_message(request, conversation_id: str, content: str):
    def parse_generated_questions(self, text):
        questions_data = []
        lines = text.split("\n")
        title = ""
        duration = 0
        passing_score = 0
        question_data = {}
        for line in lines:
            if line.startswith("Quiz Title:"):
                title = line.split(":")[1].strip()
            elif line.startswith("Duration:"):
                duration = int(line.split(":")[1].strip())
            elif line.startswith("Passing Score:"):
                passing_score_str = line.split(":")[1].strip()
                passing_score = int(passing_score_str)
            elif line.startswith("q:"):
                if question_data:
                    questions_data.append(question_data)
                    question_data = {}
                question_data["text"] = line.split(":")[1].strip()
                question_data["choices"] = []
                question_data["explanations"] = []
            elif line.startswith("c:"):
                question_data["choices"].append(line.split(":")[1].strip())
            elif line.startswith("e:"):
                question_data["explanations"].append(line.split(":")[1].strip())
            elif line.startswith("a:"):
                question_data["answer"] = int(line.split(":")[1].strip())
            elif line.startswith("w:"):
                question_data["worth"] = int(line.split(":")[1].strip())

        if question_data:
            questions_data.append(question_data)

        return {
            "title": title,
            "duration": duration,
            "passing_score": passing_score,
            "questions": questions_data,
        }

    conversation = await Conversation.objects.aget(id=conversation_id, user=request.auth)

    user_message = await Message.objects.acreate(conversation=conversation, sender="user", content=content)

    genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API_KEY)

    generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest", generation_config=generation_config, safety_settings=safety_settings)

    conversation_messages = await Message.objects.filter(conversation=conversation).order_by("timestamp").all()
    conversation_history = "\n".join([f"{message.sender}: {message.content}" for message in conversation_messages])
    home_language = request.auth.home_language.name if request.auth.home_language else "English"
    learning_language = conversation.language.name

    prompt_parts = [
        "When the user submits a request: The AI should analyze the text to identify if the request is asking for a quiz by detecting keywords such as \"quiz\", \"test\", \"questionnaire\", or \"exam\".\nIf quiz-related keywords are detected:\n- Append the tag ___QUIZ___ at the top of the response to indicate a quiz-based response.\n- Format the quiz response to include exactly five questions, and ensure each quiz contains the following elements:\n  - Quiz Title\n  - Duration: Time allocated for completing the quiz (in minutes).\n  - Passing Score: Minimum score required to pass (as an integer).\n  - Questions (q:) in the user's home language, each followed by:\n    - Choices (c:): 4 multiple-choice options for the answer in the target language.\n    - Correct Answer (a:): The index of the correct choice (0-based index), varying the position of the correct answer.\n    - Explanations (e:): Explanation for why the correct answer is right, in the user's home language.\n    - Worth (w:): Points awarded for each correct answer.\nIf no quiz-related keywords are detected:\n- Directly respond to the user's query with information or answers relevant to the request without any quiz formatting.\n\nWhen making a quiz, make sure to follow the exact format of the examples and use a variety of correct answer positions, not just the first choice.",
        "input: Quiz on Basic Vocabulary (User's Home Language: French, Learning: Italian)",
        "output: ___QUIZ___\nQuiz Title: Test de vocabulaire italien de base\nDuration: 15\nPassing Score: 80\n\nq: Comment dit-on \"livre\" en italien ?\nc: libro\nc: penna\nc: quaderno\nc: tavolo\ne: 'Libro' est le mot italien pour 'livre'.\na: 0\nw: 10\n\nq: Quel est le mot italien pour \"eau\" ?\nc: latte\nc: succo\nc: acqua\nc: vino\ne: 'Acqua' est la traduction correcte de 'eau' en italien.\na: 2\nw: 10\n\nq: Traduisez \"maison\" en italien.\nc: macchina\nc: casa\nc: cane\nc: finestra\ne: 'Casa' signifie 'maison' en italien.\na: 1\nw: 10\n\nq: Comment dit-on \"pomme\" en italien ?\nc: banana\nc: arancia\nc: mela\nc: fragola\ne: 'Mela' est le mot italien pour 'pomme'.\na: 2\nw: 10\n\nq: Quel est le mot italien pour \"chien\" ?\nc: gatto\nc: cavallo\nc: uccello\nc: cane\ne: 'Cane' est le mot italien pour 'chien'.\na: 3\nw: 10",
        "input: Quiz on Basic Phrases (User's Home Language: Dutch, Learning: English)",
        "output: ___QUIZ___\nQuiz Title: Basisuitdrukkingen in het Engels\nDuration: 12\nPassing Score: 75\n\nq: Hoe zeg je \"Hallo\" in het Engels?\nc: Hello\nc: Goodbye\nc: Thank you\nc: Good morning\ne: 'Hello' betekent 'Hallo' in het Engels.\na: 0\nw: 10\n\nq: Wat is \"Tot ziens\" in het Engels?\nc: Good morning\nc: Good night\nc: Goodbye\nc: Hello\ne: 'Goodbye' betekent 'Tot ziens' in het Engels.\na: 2\nw: 10\n\nq: Hoe zeg je \"Dank je wel\" in het Engels?\nc: Excuse me\nc: Thank you\nc: Please\nc: I don't understand\ne: 'Thank you' is Engels voor 'Dank je wel'.\na: 1\nw: 10\n\nq: Wat is \"Ja\" in het Engels?\nc: No\nc: Yes\nc: Maybe\nc: I don't know\ne: 'Yes' betekent 'Ja' in het Engels.\na: 1\nw: 10\n\nq: Hoe zeg je \"Alstublieft\" in het Engels?\nc: I'm sorry\nc: Hello\nc: Please\nc: Thank you\ne: 'Please' wordt gebruikt om 'Alstublieft' te zeggen in het Engels.\na: 2\nw: 10",
        "conversation_history " + conversation_history,
        f"input: {user_message} (User's Home Language: {home_language}, Learning: {learning_language})",
        "output: ",
    ]

    response = await model.generate_content_async(prompt_parts)

    if "___QUIZ___" in response.text:
        quiz_data = parse_generated_questions(response.text[response.text.find("___QUIZ___") + 11:])
        quiz = await Quiz.objects.acreate(
            language=conversation.language,
            user=request.auth,
            title=quiz_data["title"],
            duration=quiz_data["duration"],
            passing_score=quiz_data["passing_score"],
        )
        questions_data = quiz_data["questions"]
        for question_data in questions_data:
            question_data["quiz"] = quiz.id
            serializer = QuestionSchema(**question_data)
            await Question.objects.acreate(**serializer.dict())

        quiz_url = f"/quizzes/{quiz.id}/"
        bot_response = f"Quiz created successfully! You can take the quiz by clicking on this link: [Take the Quiz]({quiz_url})"
    else:
        bot_response = response.text.replace("\n", "\\n")

    bot_message = await Message.objects.acreate(conversation=conversation, sender="bot", content=bot_response)

    return 201, bot_message
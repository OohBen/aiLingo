import re
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt, Question, Quiz
from .serializers import AttemptSerializer, QuestionSerializer, QuizSerializer
import google.generativeai as genai
from analytics.models import UserAnalytics

class CreateQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API_KEY)

        home_language = request.user.home_language.name if request.user.home_language else "English"

        generation_config = {
        "temperature": 0.9,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        }

        safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        ]

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)

        prompt_parts = [
        "You are a language teacher responsible for creating quizzes to assess students' proficiency in various languages. You only respond using plaintext, you do not use markdown, bold, italics, lists, or anything else just plaintext. Your task is to generate a quiz with the following specifications:\n\n1. The quiz should have 5 multiple-choice questions with 4 answer choices each.\n2. The questions should focus on basic vocabulary and grammar concepts appropriate for beginners.\n3. Include the quiz title, duration in minutes, and the passing score percentage.\n4. For each question, provide an explanation for each answer choice in the language of instruction specified.\n5. Specify the point value of each question as an integer.\n\nPlease provide the quiz in the following format:\n\nQuiz Title:",
        "input: Generate a quiz titled \"French Greetings\" for English speakers learning French.",
        "output: Quiz Title: French Greetings\nDuration: 10\nPassing Score: 80\nq: How do you say \"Hello\" in French?\nc1: Bonjour\ne1: Correct! \"Bonjour\" means \"Hello\" in French.\nc2: Au revoir\ne2: \"Au revoir\" means \"Goodbye\" in French.\nc3: Merci\ne3: \"Merci\" means \"Thank you\" in French.\nc4: Bonsoir\ne4: \"Bonsoir\" means \"Good evening\" in French.\na: 1\nw: 2\nq: How do you say \"Good morning\" in French?\nc1: Bonsoir\ne1: \"Bonsoir\" means \"Good evening\" in French.\nc2: Bonjour\ne2: \"Bonjour\" is a general greeting that can be used throughout the day.\nc3: Bon matin\ne3: Correct! \"Bon matin\" means \"Good morning\" in French.\nc4: Bonne nuit\ne4: \"Bonne nuit\" means \"Good night\" in French.\na: 3\nw: 2\nq: What is the French word for \"please\"?\nc1: Merci\ne1: \"Merci\" means \"Thank you\" in French.\nc2: S'il vous plaît\ne2: Correct! \"S'il vous plaît\" means \"Please\" in French.\nc3: Oui\ne3: \"Oui\" means \"Yes\" in French.\nc4: Non\ne4: \"Non\" means \"No\" in French.\na: 2\nw: 2\nq: How do you say \"My name is...\" in French?\nc1: Je m'appelle...\ne1: Correct! \"Je m'appelle...\" means \"My name is...\" in French.\nc2: Quel est votre nom?\ne2: \"Quel est votre nom?\" means \"What is your name?\" in French.\nc3: Comment allez-vous?\ne3: \"Comment allez-vous?\" means \"How are you?\" in French.\nc4: Merci\ne4: \"Merci\" means \"Thank you\" in French.\na: 1\nw: 3\nq: What is the French phrase for \"Have a nice day\"?\nc1: Bonne journée\ne1: Correct! \"Bonne journée\" means \"Have a nice day\" in French.\nc2: Bon appétit\ne2: \"Bon appétit\" means \"Enjoy your meal\" in French.\nc3: Au revoir\ne3: \"Au revoir\" means \"Goodbye\" in French.\nc4: Bien sûr\ne4: \"Bien sûr\" means \"Of course\" in French.\na: 1\nw: 3",
        "input: Generate a quiz titled \"Gli Articoli\" for English speakers learning French.",
        "output: Quiz Title: Gli Articoli\nDuration: 12\nPassing Score: 75\nq: What is the definite article for \"il libro\" (the book) in Italian?\nc1: il\ne1: Correct! \"Il\" is the definite article for masculine singular nouns in Italian.\nc2: la\ne2: \"La\" is the definite article for feminine singular nouns in Italian.\nc3: i\ne3: \"I\" is the definite article for masculine plural nouns in Italian.\nc4: le\ne4: \"Le\" is the definite article for feminine plural nouns in Italian.\na: 1\nw: 2q: What is the indefinite article for \"una penna\" (a pen) in Italian?\nc1: il\ne1: \"Il\" is the definite article for masculine singular nouns in Italian.\nc2: un\ne2: Correct! \"Un\" is the indefinite article for masculine singular nouns in Italian.\nc3: una\ne3: \"Una\" is the indefinite article for feminine singular nouns in Italian.\nc4: dei\ne4: \"Dei\" is the plural indefinite article for masculine nouns in Italian.\na: 2\nw: 2\nq: Which article should be used before \"studenti\" (students)?\nc1: il\ne1: \"Il\" is for singular masculine nouns in Italian.\nc2: la\ne2: \"La\" is for singular feminine nouns in Italian.\nc3: i\ne3: Correct! \"I\" is the definite plural article for masculine nouns like \"studenti\".\nc4: le\ne4: \"Le\" is the definite plural article for feminine nouns in Italian.\na: 3\nw: 3\nq: What is the correct way to say \"the girls\" in Italian?\nc1: i ragazze\ne1: This is incorrect. \"I\" is for masculine plural nouns.\nc2: la ragazze\ne2: This is incorrect. \"La\" is for singular feminine nouns.\nc3: le ragazze\ne3: Correct! \"Le ragazze\" means \"the girls\" using the feminine plural article.\nc4: un ragazze\ne4: This is incorrect. \"Un\" is the indefinite masculine singular article.\na: 3\nw: 2\nq: How do you say \"a book\" in Italian?\nc1: il libro\ne1: \"Il libro\" means \"the book\" using the definite article.\nc2: un libro\ne2: Correct! \"Un libro\" means \"a book\" using the indefinite masculine singular article.\nc3: una libro\ne3: This is incorrect. \"Una\" is for feminine singular nouns.\nc4: i libri\ne4: \"I libri\" means \"the books\" using the masculine plural definite article.\na: 2\nw: 3",
        "input: Generate a quiz titled \"Del español al alemán\" for Spanish speakers learning German.",
        "output: Quiz Title: Del español al alemán\nDuration: 20\nPassing Score: 75\nq: How do you say \"Hola\" (Hello) in German?\nc1: Tschüss\ne1: \"Tschüss\" means \"Goodbye\" in German.\nc2: Hallo\ne2: Correct! \"Hallo\" means \"Hello\" in German.\nc3: Guten Tag\ne3: \"Guten Tag\" means \"Good day\" in German.\nc4: Danke\ne4: \"Danke\" means \"Thank you\" in German.\na: 2\nw: 2\nq: What is the German translation for \"Gracias\" (Thank you)?\nc1: Bitte\ne1: \"Bitte\" means \"Please\" in German.\nc2: Nein\ne2: \"Nein\" means \"No\" in German.\nc3: Danke\ne3: Correct! \"Danke\" means \"Thank you\" in German.\nc4: Ja\ne4: \"Ja\" means \"Yes\" in German.\na: 3\nw: 2\nq: How would you say \"El perro\" (The dog) in German?\nc1: Der Hund\ne1: Correct! \"Der Hund\" means \"The dog\" in German.\nc2: Die Katze\ne2: \"Die Katze\" means \"The cat\" in German.\nc3: Das Pferd\ne3: \"Das Pferd\" means \"The horse\" in German.\nc4: Die Maus\ne4: \"Die Maus\" means \"The mouse\" in German.\na: 1\nw: 3\nq: Translate \"Comer\" (To eat) to German.\nc1: Trinken\ne1: \"Trinken\" means \"To drink\" in German.\nc2: Essen\ne2: Correct! \"Essen\" means \"To eat\" in German.\nc3: Schlafen\ne3: \"Schlafen\" means \"To sleep\" in German.\nc4: Lesen\ne4: \"Lesen\" means \"To read\" in German.\na: 2\nw: 3\nq: How do you say \"La casa\" (The house) in German?\nc1: Das Haus\ne1: Correct! \"Das Haus\" means \"The house\" in German.\nc2: Der Baum\ne2: \"Der Baum\" means \"The tree\" in German.\nc3: Die Blume\ne3: \"Die Blume\" means \"The flower\" in German.\nc4: Der Apfel\ne4: \"Der Apfel\" means \"The apple\" in German.\na: 1\nw: 2",
        f"input: Generate a quiz titled \"{request.data['title']}\" for {home_language} speakers learning {request.data['language']}.",
        "output: ",
        ]

        response = model.generate_content(prompt_parts)

        generated_text = response.text.strip()

        quiz_data = self.parse_generated_questions(generated_text)
        
        quiz = Quiz.objects.create(
            user=self.request.user,
            title=quiz_data.get("title"),
            duration=quiz_data.get("duration"),
            passing_score=quiz_data.get("passing_score"),
            language_id=request.data["language"],
        )
        quiz.save()

        questions_data = quiz_data.get("questions", [])
        for question_data in questions_data:
            serializer = QuestionSerializer(data=question_data)
            serializer.is_valid(raise_exception=True)
            question = serializer.save(quiz=quiz)

        quiz_serializer = QuizSerializer(quiz)
        return Response(quiz_serializer.data, status=status.HTTP_201_CREATED)

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
                passing_score = int(line.split(":")[1].strip())
            elif line.startswith("q:"):
                if question_data:
                    questions_data.append(question_data)
                question_data = {"text": line.split(":")[1].strip(), "choices": [], "explanations": [], "worth": 1}
            elif line.startswith("c"):
                question_data["choices"].append(line.split(":")[1].strip())
            elif line.startswith("e"):
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
        
class QuizListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizQuestionsView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs["quiz_id"]
        return Question.objects.filter(quiz_id=quiz_id)

class QuizAttemptView(generics.CreateAPIView):
    serializer_class = AttemptSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        quiz_id = request.data.get("quiz")
        user_answers = request.data.get("user_answers")

        quiz = Quiz.objects.get(id=quiz_id)
        user = request.user

        total_score = 0
        max_score = 0

        for question_id, user_answer in user_answers.items():
            question = Question.objects.get(id=question_id)
            max_score += question.worth
            if question.answer == user_answer:
                total_score += question.worth

        score = (total_score / max_score) * 100
        attempt = Attempt.objects.create(user=user, quiz=quiz, score=score)
        serializer = self.get_serializer(attempt)

        topic_scores = {}
        for question in quiz.question_set.all():
            if question.answer == user_answers.get(str(question.id)):
                topic_scores[question.text] = question.worth

        user_analytics, _ = UserAnalytics.objects.get_or_create(user=user)
        user_analytics.update_quiz_analytics(quiz.language, score, topic_scores)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
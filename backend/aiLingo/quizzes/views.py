import re
from django.conf import settings
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Attempt, Question, Quiz
from .serializers import AttemptSerializer, QuestionSerializer, QuizSerializer
import google.generativeai as genai
from analytics.models import UserAnalytics
from languages.models import Language

class CreateQuizView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API_KEY)

        home_language = request.user.home_language.name if request.user.home_language else "English"
        learning_language = Language.objects.get(id=request.data["language"]).name
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

        model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                    generation_config=generation_config,
                                    safety_settings=safety_settings)


        prompt_parts = [
            "You are a language teacher responsible for creating quizzes to assess students' proficiency in various languages. You only respond using plaintext, you do not use markdown, bold, italics, lists, or anything else just plaintext. Your task is to generate a quiz with the following specifications:\n\n1. The quiz should have 5 multiple-choice questions with 4 answer choices each.\n2. The questions should focus on basic vocabulary and grammar concepts appropriate for beginners.\n3. Include the quiz title, duration in minutes, and the passing score as an integer.\n4. The questions should be in the user's home language, and the answer choices should be in the target language they are learning.\n5. For each question, provide an explanation for the correct answer in the user's home language.\n6. Specify the point value of each question as an integer.\n\nPlease provide the quiz in the following format:\n\nQuiz Title:",
            "input: Generate a quiz titled \"French Greetings\" for English speakers learning French.",
            "output: Quiz Title: French Greetings\nDuration: 10\nPassing Score: 80\nq: How do you say \"Hello\" in French?\nc: Bonjour\nc: Au revoir\nc: Merci\nc: Bonsoir\ne: \"Bonjour\" means \"Hello\" in French.\na: 0\nw: 2\nq: What is the French phrase for \"Good morning\"?\nc: Bonsoir\nc: Bon matin\nc: Bonjour\nc: Bonne nuit\ne: \"Bon matin\" means \"Good morning\" in French.\na: 1\nw: 2\nq: How do you say \"please\" in French?\nc: Merci\nc: S'il vous plaît\nc: Oui\nc: Non\ne: \"S'il vous plaît\" means \"Please\" in French.\na: 1\nw: 2\nq: What is the French translation of \"My name is...\"?\nc: Je m'appelle...\nc: Quel est votre nom?\nc: Comment allez-vous?\nc: Merci\ne: \"Je m'appelle...\" means \"My name is...\" in French.\na: 0\nw: 3\nq: How do you say \"Have a nice day\" in French?\nc: Bonne journée\nc: Bon appétit\nc: Au revoir\nc: Bien sûr\ne: \"Bonne journée\" means \"Have a nice day\" in French.\na: 0\nw: 3",
            "input: Generate a quiz titled \"Gli Articoli\" for English speakers learning Italian.",
            "output: Quiz Title: Gli Articoli\nDuration: 12\nPassing Score: 75\nq: What is the definite article for \"the book\" in Italian?\nc: il libro\nc: la penna\nc: i quaderni\nc: le tavole\ne: \"il\" is the definite article for masculine singular nouns like \"libro\".\na: 0\nw: 2\nq: What is the indefinite article for \"a pen\" in Italian?\nc: il libro\nc: un libro\nc: una penna\nc: dei libri\ne: \"una\" is the indefinite article for feminine singular nouns like \"penna\".\na: 2\nw: 2\nq: Which article should be used before the plural masculine noun \"students\"?\nc: il\nc: la\nc: i\nc: le\ne: \"i\" is the definite plural article for masculine nouns like \"studenti\".\na: 2\nw: 3\nq: What is the correct way to say \"the girls\" in Italian?\nc: i ragazze\nc: la ragazza\nc: le ragazze\nc: un ragazzo\ne: \"le\" is the definite plural article for feminine nouns like \"ragazze\".\na: 2\nw: 2\nq: How do you say \"a book\" in Italian?\nc: il libro\nc: un libro\nc: una libro\nc: i libri\ne: \"un\" is the indefinite masculine singular article used for \"libro\".\na: 1\nw: 3",
            "input: Generate a quiz titled \"Del español al alemán\" for Spanish speakers learning German.",
            "output: Quiz Title: Del español al alemán\nDuration: 20\nPassing Score: 75\nq: ¿Cómo se dice \"Hola\" en alemán?\nc: Tschüss\nc: Hallo\nc: Guten Tag\nc: Danke\ne: \"Hallo\" significa \"Hola\" en alemán.\na: 1\nw: 2\nq: ¿Cuál es la traducción al alemán de \"Gracias\"?\nc: Bitte\nc: Nein\nc: Danke\nc: Ja\ne: \"Danke\" significa \"Gracias\" en alemán.\na: 2\nw: 2\nq: ¿Cómo se diría \"El perro\" en alemán?\nc: Der Hund\nc: Die Katze\nc: Das Pferd\nc: Die Maus\ne: \"Der Hund\" significa \"El perro\" en alemán.\na: 0\nw: 3\nq: Traduce \"Comer\" al alemán.\nc: Trinken\nc: Essen\nc: Schlafen\nc: Lesen\ne: \"Essen\" significa \"Comer\" en alemán.\na: 1\nw: 3\nq: ¿Cómo se dice \"La casa\" en alemán?\nc: Das Haus\nc: Der Baum\nc: Die Blume\nc: Der Apfel\ne: \"Das Haus\" significa \"La casa\" en alemán.\na: 0\nw: 2",
            "input: Generate a quiz titled \"Vocabulario básico\" for beginner Spanish learners whose native language is English.",
            "output: Quiz Title: Vocabulario básico\nDuration: 10\nPassing Score: 70\nq: What is the Spanish word for \"hello\"?\nc: Adiós\nc: Hola\nc: Gracias\nc: Sí\ne: \"Hola\" means \"hello\" in Spanish.\na: 1\nw: 2\nq: How do you say \"water\" in Spanish?\nc: Leche\nc: Jugo\nc: Agua\nc: Vino\ne: \"Agua\" means \"water\" in Spanish.\na: 2\nw: 2\nq: What is the Spanish translation for \"book\"?\nc: Lápiz\nc: Libro\nc: Mochila\nc: Regla\ne: \"Libro\" means \"book\" in Spanish.\na: 1\nw: 3\nq: Translate \"apple\" to Spanish.\nc: Plátano\nc: Naranja\nc: Manzana\nc: Sandía\ne: \"Manzana\" means \"apple\" in Spanish.\na: 2\nw: 2\nq: How would you say \"house\" in Spanish?\nc: Carro\nc: Casa\nc: Perro\nc: Escuela\ne: \"Casa\" means \"house\" in Spanish.\na: 1\nw: 3",
            "input: Generate a quiz titled \"El Subjuntivo\" for English speakers learning Spanish.",
            "output: Quiz Title: El Subjuntivo\nDuration: 15\nPassing Score: 75\nq: Which verb form correctly completes the sentence \"I want you to come with me\" in Spanish?\nc: vienes\nc: vengas\nc: viniste\nc: vendrás\ne: \"vengas\" is the present subjunctive form, used for wishes, desires, or uncertainty.\na: 1\nw: 3\nq: Choose the correct subjunctive form of the verb \"ser\" (to be) in the sentence \"It's important that you be honest\" in Spanish.\nc: eres\nc: seas\nc: fuiste\nc: serás\ne: \"seas\" is the present subjunctive form of \"ser\", used for expressing importance or necessity.\na: 1\nw: 3\nq: Which sentence correctly uses the subjunctive mood in Spanish?\nc: Creo que ella es inteligente.\nc: Es posible que él venga mañana.\nc: Sé que ellos viven en Madrid.\nc: Estoy seguro de que aprobará el examen.\ne: The sentence \"Es posible que él venga mañana\" uses the subjunctive mood to express possibility or uncertainty.\na: 1\nw: 3\nq: Complete the sentence with the correct subjunctive form in Spanish: \"I hope the weather is good tomorrow\".\nc: hace\nc: haga\nc: hizo\nc: hará\ne: \"haga\" is the present subjunctive form of \"hacer\", used to express hopes or wishes.\na: 1\nw: 3\nq: Choose the correct verb form for the sentence \"I suggest that you exercise more\" in Spanish.\nc: haces\nc: hagas\nc: hiciste\nc: harás\ne: \"hagas\" is the present subjunctive form of \"hacer\", used for giving suggestions or advice.\na: 1\nw: 3",
            "input: Generate a quiz titled \"Präpositionen\" for English speakers learning German.",
            "output: Quiz Title: Präpositionen\nDuration: 12\nPassing Score: 80\nq: Which preposition correctly completes the sentence \"I'm going home\" in German?\nc: zu Hause\nc: auf Hause\nc: in Hause\nc: an Hause\ne: \"zu\" is used to indicate movement towards a destination, such as \"to\" or \"towards\" in English.\na: 0\nw: 3\nq: Choose the correct preposition for the sentence \"The book is lying on the table\" in German.\nc: in dem Tisch\nc: an dem Tisch\nc: auf dem Tisch\nc: über dem Tisch\ne: \"auf\" means \"on\" or \"onto\" in English, usually referring to a surface or a direction upwards.\na: 2\nw: 3\nq: Which preposition is used in the sentence \"I come from Berlin\" in German?\nc: aus Berlin\nc: von Berlin\nc: bei Berlin\nc: nach Berlin\ne: \"aus\" is used to indicate origin or source, such as \"from\" or \"out of\" in English.\na: 0\nw: 3\nq: Complete the sentence with the correct preposition in German: \"He is waiting for his girlfriend\".\nc: für seine Freundin\nc: um seine Freundin\nc: auf seine Freundin\nc: zu seine Freundin\ne: \"auf\" is used with the verb \"warten\" (to wait) to mean \"for\" in English.\na: 2\nw: 3\nq: Choose the correct preposition for the sentence \"We are going on vacation\" in German.\nc: in den Urlaub\nc: an den Urlaub\nc: auf den Urlaub\nc: zu den Urlaub\ne: \"in\" is used with the accusative case to indicate a destination or a period of time, such as \"on\" vacation.\na: 0\nw: 3",
            "input: Generate a quiz titled \"Cooking Vocabulary\" for Italian speakers learning English.",
            "output: Quiz Title: Cooking Vocabulary\nDuration: 10\nPassing Score: 80\nq: Come si dice \"friggere\" in inglese?\nc: Boil\nc: Bake\nc: Fry\nc: Grill\ne: \"Fry\" significa \"friggere\" in inglese.\na: 2\nw: 2\nq: Qual è la traduzione di \"mescolare\" in inglese?\nc: Mix\nc: Blend\nc: Stir\nc: Beat\ne: \"Stir\" significa \"mescolare\" in inglese.\na: 2\nw: 2\nq: Come si traduce \"pentola\" in inglese?\nc: Pan\nc: Pot\nc: Kettle\nc: Bowl\ne: \"Pot\" significa \"pentola\" in inglese.\na: 1\nw: 3\nq: Qual è la traduzione di \"affettare\" in inglese?\nc: Cut\nc: Chop\nc: Slice\nc: Dice\ne: \"Slice\" significa \"affettare\" in inglese.\na: 2\nw: 2\nq: Come si dice \"grattugiare\" in inglese?\nc: Grind\nc: Shred\nc: Mince\nc: Grate\ne: \"Grate\" significa \"grattugiare\" in inglese.\na: 3\nw: 2",
            f"input: Generate a quiz about {learning_language} {request.data['title']} for {home_language} speakers learning {request.data['language']} title it appropriately. Passing score must be an integer not a percent, same with the time just an integer amount of minutes. Follow the examples given exactly in that format. In addition please make sure if a quiz is made all the questions ande explanations are made {home_language} and all the answers made in {request.data['language']}",
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
                passing_score_str = line.split(":")[1].strip()
                passing_score = int(passing_score_str)
            elif line.startswith("q:"):
                if question_data:
                    questions_data.append(question_data)
                    question_data = {}
                question_data["text"] = line.split(":")[1].strip()
                question_data["choices"] = []
                question_data["explanations"] = []
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
    serializer_class = QuizSerializer

    def get_queryset(self):
        user = self.request.user
        return Quiz.objects.filter(user=user)

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
        result = []

        for question in quiz.question_set.all():
            user_answer = user_answers.get(str(question.id))
            max_score += question.worth
            if question.answer == user_answer:
                total_score += question.worth
            result.append({
                'question': question.text,
                'user_answer_index': user_answer,
                'user_answer': question.choices[user_answer] if user_answer is not None and user_answer < len(question.choices) else None,
                'correct_answer_index': question.answer,
                'correct_answer': question.choices[question.answer] if question.answer < len(question.choices) else None,
                'explanation': question.explanations[question.answer] if question.explanations and question.answer < len(question.explanations) else None,
            })

        score = (total_score / max_score) * 100
        attempt = Attempt.objects.create(user=user, quiz=quiz, score=score)
        serializer = self.get_serializer(attempt)

        return Response({
            'attempt': serializer.data,
            'result': result,
        }, status=status.HTTP_201_CREATED)
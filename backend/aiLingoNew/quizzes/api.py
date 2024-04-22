import re
from django.conf import settings
from ninja import Router
from ninja.responses import codes_4xx

from backend.aiLingoNew.users.api import AuthBearer
from .models import Attempt, Question, Quiz
from .schemas import AttemptSchema, QuestionSchema, QuizSchema
import google.generativeai as genai
from analytics.models import UserAnalytics

router = Router()

@router.post("/create", response=QuizSchema)
async def create_quiz(request, payload: QuizSchema):
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

    genai.configure(api_key=settings.GOOGLE_GENERATIVE_AI_API_KEY)

    home_language = request.auth.home_language.name if request.auth.home_language else "English"

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
    "You are a language teacher responsible for creating quizzes to assess students' proficiency in various languages. You only respond using plaintext, you do not use markdown, bold, italics, lists, or anything else just plaintext. Your task is to generate a quiz with the following specifications:\n\n1. The quiz should have 5 multiple-choice questions with 4 answer choices each.\n2. The questions should focus on basic vocabulary and grammar concepts appropriate for beginners.\n3. Include the quiz title, duration in minutes, and the passing score percentage.\n4. For each question, provide an explanation for each answer choice in the language of instruction specified.\n5. Specify the point value of each question as an integer.\n\nPlease provide the quiz in the following format:\n\nQuiz Title:",
    "input: Generate a quiz titled \"French Greetings\" for English speakers learning French.",
    "output: Quiz Title: French Greetings\nDuration: 10\nPassing Score: 80\nq: How do you say \"Hello\" in French?\nc1: Bonjour\ne1: Correct! \"Bonjour\" means \"Hello\" in French.\nc2: Au revoir\ne2: \"Au revoir\" means \"Goodbye\" in French.\nc3: Merci\ne3: \"Merci\" means \"Thank you\" in French.\nc4: Bonsoir\ne4: \"Bonsoir\" means \"Good evening\" in French.\na: 1\nw: 2\nq: How do you say \"Good morning\" in French?\nc1: Bonsoir\ne1: \"Bonsoir\" means \"Good evening\" in French.\nc2: Bonjour\ne2: \"Bonjour\" is a general greeting that can be used throughout the day.\nc3: Bon matin\ne3: Correct! \"Bon matin\" means \"Good morning\" in French.\nc4: Bonne nuit\ne4: \"Bonne nuit\" means \"Good night\" in French.\na: 3\nw: 2\nq: What is the French word for \"please\"?\nc1: Merci\ne1: \"Merci\" means \"Thank you\" in French.\nc2: S'il vous plaît\ne2: Correct! \"S'il vous plaît\" means \"Please\" in French.\nc3: Oui\ne3: \"Oui\" means \"Yes\" in French.\nc4: Non\ne4: \"Non\" means \"No\" in French.\na: 2\nw: 2\nq: How do you say \"My name is...\" in French?\nc1: Je m'appelle...\ne1: Correct! \"Je m'appelle...\" means \"My name is...\" in French.\nc2: Quel est votre nom?\ne2: \"Quel est votre nom?\" means \"What is your name?\" in French.\nc3: Comment allez-vous?\ne3: \"Comment allez-vous?\" means \"How are you?\" in French.\nc4: Merci\ne4: \"Merci\" means \"Thank you\" in French.\na: 1\nw: 3\nq: What is the French phrase for \"Have a nice day\"?\nc1: Bonne journée\ne1: Correct! \"Bonne journée\" means \"Have a nice day\" in French.\nc2: Bon appétit\ne2: \"Bon appétit\" means \"Enjoy your meal\" in French.\nc3: Au revoir\ne3: \"Au revoir\" means \"Goodbye\" in French.\nc4: Bien sûr\ne4: \"Bien sûr\" means \"Of course\" in French.\na: 1\nw: 3",
    "input: Generate a quiz titled \"Gli Articoli\" for English speakers learning French.",
    "output: Quiz Title: Gli Articoli\nDuration: 12\nPassing Score: 75\nq: What is the definite article for \"il libro\" (the book) in Italian?\nc1: il\ne1: Correct! \"Il\" is the definite article for masculine singular nouns in Italian.\nc2: la\ne2: \"La\" is the definite article for feminine singular nouns in Italian.\nc3: i\ne3: \"I\" is the definite article for masculine plural nouns in Italian.\nc4: le\ne4: \"Le\" is the definite article for feminine plural nouns in Italian.\na: 1\nw: 2q: What is the indefinite article for \"una penna\" (a pen) in Italian?\nc1: il\ne1: \"Il\" is the definite article for masculine singular nouns in Italian.\nc2: un\ne2: Correct! \"Un\" is the indefinite article for masculine singular nouns in Italian.\nc3: una\ne3: \"Una\" is the indefinite article for feminine singular nouns in Italian.\nc4: dei\ne4: \"Dei\" is the plural indefinite article for masculine nouns in Italian.\na: 2\nw: 2\nq: Which article should be used before \"studenti\" (students)?\nc1: il\ne1: \"Il\" is for singular masculine nouns in Italian.\nc2: la\ne2: \"La\" is for singular feminine nouns in Italian.\nc3: i\ne3: Correct! \"I\" is the definite plural article for masculine nouns like \"studenti\".\nc4: le\ne4: \"Le\" is the definite plural article for feminine nouns in Italian.\na: 3\nw: 3\nq: What is the correct way to say \"the girls\" in Italian?\nc1: i ragazze\ne1: This is incorrect. \"I\" is for masculine plural nouns.\nc2: la ragazze\ne2: This is incorrect. \"La\" is for singular feminine nouns.\nc3: le ragazze\ne3: Correct! \"Le ragazze\" means \"the girls\" using the feminine plural article.\nc4: un ragazze\ne4: This is incorrect. \"Un\" is the indefinite masculine singular article.\na: 3\nw: 2\nq: How do you say \"a book\" in Italian?\nc1: il libro\ne1: \"Il libro\" means \"the book\" using the definite article.\nc2: un libro\ne2: Correct! \"Un libro\" means \"a book\" using the indefinite masculine singular article.\nc3: una libro\ne3: This is incorrect. \"Una\" is for feminine singular nouns.\nc4: i libri\ne4: \"I libri\" means \"the books\" using the masculine plural definite article.\na: 2\nw: 3",
    "input: Generate a quiz titled \"Del español al alemán\" for Spanish speakers learning German.",
    "output: Quiz Title: Del español al alemán\nDuration: 20\nPassing Score: 75\nq: How do you say \"Hola\" (Hello) in German?\nc1: Tschüss\ne1: \"Tschüss\" means \"Goodbye\" in German.\nc2: Hallo\ne2: Correct! \"Hallo\" means \"Hello\" in German.\nc3: Guten Tag\ne3: \"Guten Tag\" means \"Good day\" in German.\nc4: Danke\ne4: \"Danke\" means \"Thank you\" in German.\na: 2\nw: 2q: What is the German translation for \"Gracias\" (Thank you)?\nc1: Bitte\ne1: \"Bitte\" means \"Please\" in German.\nc2: Nein\ne2: \"Nein\" means \"No\" in German.\nc3: Danke\ne3: Correct! \"Danke\" means \"Thank you\" in German.\nc4: Ja\ne4: \"Ja\" means \"Yes\" in German.\na: 3\nw: 2q: How would you say \"El perro\" (The dog) in German?\nc1: Der Hund\ne1: Correct! \"Der Hund\" means \"The dog\" in German.\nc2: Die Katze\ne2: \"Die Katze\" means \"The cat\" in German.\nc3: Das Pferd\ne3: \"Das Pferd\" means \"The horse\" in German.\nc4: Die Maus\ne4: \"Die Maus\" means \"The mouse\" in German.\na: 1\nw: 3q: Translate \"Comer\" (To eat) to German.\nc1: Trinken\ne1: \"Trinken\" means \"To drink\" in German.\nc2: Essen\ne2: Correct! \"Essen\" means \"To eat\" in German.\nc3: Schlafen\ne3: \"Schlafen\" means \"To sleep\" in German.\nc4: Lesen\ne4: \"Lesen\" means \"To read\" in German.\na: 2\nw: 3q: How do you say \"La casa\" (The house) in German?\nc1: Das Haus\ne1: Correct! \"Das Haus\" means \"The house\" in German.\nc2: Der Baum\ne2: \"Der Baum\" means \"The tree\" in German.\nc3: Die Blume\ne3: \"Die Blume\" means \"The flower\" in German.\nc4: Der Apfel\ne4: \"Der Apfel\" means \"The apple\" in German.\na: 1\nw: 2Prompt: Create an English to Spanish vocabulary quiz titled \"Vocabulario básico\" for beginner Spanish learners.Quiz Title: Vocabulario básico\nDuration: 10\nPassing Score: 70q: What is the Spanish word for \"hello\"?\nc1: Adiós\ne1: \"Adiós\" means \"goodbye\" in Spanish.\nc2: Hola\ne2: Correct! \"Hola\" means \"hello\" in Spanish.\nc3: Gracias\ne3: \"Gracias\" means \"thank you\" in Spanish.\nc4: Sí\ne4: \"Sí\" means \"yes\" in Spanish.\na: 2\nw: 2q: How do you say \"water\" in Spanish?\nc1: Leche\ne1: \"Leche\" means \"milk\" in Spanish.\nc2: Jugo\ne2: \"Jugo\" means \"juice\" in Spanish.\nc3: Agua\ne3: Correct! \"Agua\" means \"water\" in Spanish.\nc4: Vino\ne4: \"Vino\" means \"wine\" in Spanish.\na: 3\nw: 2q: What is the Spanish translation for \"book\"?\nc1: Lápiz\ne1: \"Lápiz\" means \"pencil\" in Spanish.\nc2: Libro\ne2: Correct! \"Libro\" means \"book\" in Spanish.\nc3: Mochila\ne3: \"Mochila\" means \"backpack\" in Spanish.\nc4: Regla\ne4: \"Regla\" means \"ruler\" in Spanish.\na: 2\nw: 3q: Translate \"apple\" to Spanish.\nc1: Plátano\ne1: \"Plátano\" means \"banana\" in Spanish.\nc2: Naranja\ne2: \"Naranja\" means \"orange\" in Spanish.\nc3: Manzana\ne3: Correct! \"Manzana\" means \"apple\" in Spanish.\nc4: Sandía\ne4: \"Sandía\" means \"watermelon\" in Spanish.\na: 3\nw: 2q: How would you say \"house\" in Spanish?\nc1: Carro\ne1: \"Carro\" means \"car\" in Spanish.\nc2: Casa\ne2: Correct! \"Casa\" means \"house\" in Spanish.\nc3: Perro\ne3: \"Perro\" means \"dog\" in Spanish.\nc4: Escuela\ne4: \"Escuela\" means \"school\" in Spanish.\na: 2\nw: 3",
    "input: Generate a quiz titled \"El Subjuntivo\" for English speakers learning Spanish.",
    "output: Quiz Title: El Subjuntivo\nDuration: 15\nPassing Score: 75\nq: Which verb form correctly completes the sentence \"Quiero que tú _____ conmigo\" (I want you to come with me)?\nc1: vienes\ne1: \"Vienes\" is the present indicative form, used for facts or certainty.\nc2: vengas\ne2: Correct! \"Vengas\" is the present subjunctive form, used for wishes, desires, or uncertainty.\nc3: viniste\ne3: \"Viniste\" is the preterite indicative form, used for completed actions in the past.\nc4: vendrás\ne4: \"Vendrás\" is the future indicative form, used for actions that will happen in the future.\na: 2\nw: 3\nq: Choose the correct subjunctive form of the verb \"ser\" (to be) in the sentence \"Es importante que _____ honesto\" (It's important that you be honest).\nc1: eres\ne1: \"Eres\" is the present indicative form, used for facts or certainty.\nc2: seas\ne2: Correct! \"Seas\" is the present subjunctive form, used for wishes, desires, or uncertainty.\nc3: fuiste\ne3: \"Fuiste\" is the preterite indicative form, used for completed actions in the past.\nc4: serás\ne4: \"Serás\" is the future indicative form, used for actions that will happen in the future.\na: 2\nw: 3\nq: Which sentence correctly uses the subjunctive mood?\nc1: Creo que ella es inteligente.\ne1: This sentence uses the indicative mood, stating a fact or belief.\nc2: Es posible que él venga mañana.\ne2: Correct! This sentence uses the subjunctive mood to express possibility or uncertainty.\nc3: Sé que ellos viven en Madrid.\ne3: This sentence uses the indicative mood, stating a known fact.\nc4: Estoy seguro de que aprobará el examen.\ne4: This sentence uses the indicative mood, expressing certainty about a future event.\na: 2\nw: 3\nq: Complete the sentence with the correct subjunctive form: \"Ojalá _____ buen tiempo mañana\" (I hope the weather is good tomorrow).\nc1: hace\ne1: \"Hace\" is the present indicative form, used for facts or certainty.\nc2: haga\ne2: Correct! \"Haga\" is the present subjunctive form, used for wishes, desires, or uncertainty.\nc3: hizo\ne3: \"Hizo\" is the preterite indicative form, used for completed actions in the past.\nc4: hará\ne4: \"Hará\" is the future indicative form, used for actions that will happen in the future.\na: 2\nw: 3\nq: Choose the correct verb form for the sentence \"Te sugiero que _____ más ejercicio\" (I suggest that you exercise more).\nc1: haces\ne1: \"Haces\" is the present indicative form, used for facts or certainty.\nc2: hagas\ne2: Correct! \"Hagas\" is the present subjunctive form, used for suggestions, advice, or uncertainty.\nc3: hiciste\ne3: \"Hiciste\" is the preterite indicative form, used for completed actions in the past.\nc4: harás\ne4: \"Harás\" is the future indicative form, used for actions that will happen in the future.\na: 2\nw: 3",
    "input: Generate a quiz titled \"Präpositionen\" for English speakers learning German.",
    "output: Quiz Title: Präpositionen\nDuration: 12\nPassing Score: 80\nq: Which preposition correctly completes the sentence \"Ich gehe _____ Hause\" (I'm going home)?\nc1: zu\ne1: Correct! \"Zu\" is used to indicate movement towards a destination, such as \"to\" or \"towards\" in English.\nc2: auf\ne2: \"Auf\" means \"on\" or \"onto\" in English, usually referring to a surface or a direction upwards.\nc3: in\ne3: \"In\" is used to indicate location inside something, such as \"in\" or \"into\" in English.\nc4: an\ne4: \"An\" is used to indicate proximity or contact, such as \"at,\" \"on,\" or \"by\" in English.\na: 1\nw: 3\nq: Choose the correct preposition for the sentence \"Das Buch liegt _____ dem Tisch\" (The book is lying on the table).\nc1: in\ne1: \"In\" is used to indicate location inside something, such as \"in\" or \"into\" in English.\nc2: an\ne2: \"An\" is used to indicate proximity or contact, such as \"at,\" \"on,\" or \"by\" in English.\nc3: auf\ne3: Correct! \"Auf\" means \"on\" or \"onto\" in English, usually referring to a surface or a direction upwards.\nc4: über\ne4: \"Über\" means \"over\" or \"above\" in English, indicating a higher position without contact.\na: 3\nw: 3\nq: Which preposition is used in the sentence \"Ich komme _____ Berlin\" (I come from Berlin)?\nc1: aus\ne1: Correct! \"Aus\" is used to indicate origin or source, such as \"from\" or \"out of\" in English.\nc2: von\ne2: \"Von\" also means \"from\" in English but is used differently than \"aus,\" often with people or in abstract contexts.\nc3: bei\ne3: \"Bei\" means \"at,\" \"near,\" or \"with\" in English, often referring to people or locations.\nc4: nach\ne4: \"Nach\" means \"to\" or \"towards\" in English, indicating direction or destination.\na: 1\nw: 3\nq: Complete the sentence with the correct preposition: \"Er wartet _____ seine Freundin\" (He is waiting for his girlfriend).\nc1: für\ne1: \"Für\" means \"for\" in English, but it is used to indicate purpose, benefit, or a recipient.\nc2: um\ne2: \"Um\" means \"around\" or \"at\" in English, often referring to time or location.\nc3: auf\ne3: Correct! \"Auf\" is used with the verb \"warten\" (to wait) to mean \"for\" in English.\nc4: zu\ne4: \"Zu\" is used to indicate movement towards a destination, such as \"to\" or \"towards\" in English.\na: 3\nw: 3\nq: Choose the correct preposition for the sentence \"Wir fahren _____ den Urlaub\" (We are going on vacation).\nc1: in\ne1: Correct! \"In\" is used with the accusative case to indicate a destination or a period of time, such as \"on\" vacation.\nc2: an\ne2: \"An\" is used to indicate proximity or contact, such as \"at,\" \"on,\" or \"by\" in English.\nc3: auf\ne3: \"Auf\" means \"on\" or \"onto\" in English, usually referring to a surface or a direction upwards.\nc4: zu\ne4: \"Zu\" is used to indicate movement towards a destination, such as \"to\" or \"towards\" in English.\na: 1\nw: 3",
    "input: Generate a quiz titled \"Cooking Vocabulary\" for Italian speakers learning English",
    "output: Quiz Title: Cooking Vocabulary\nDuration: 10\nPassing Score: 80\nq: What is the English word for \"friggere\" (to fry)?\nc1: Boil\ne1: \"Boil\" significa \"bollire\" in italiano, non \"friggere\".\nc2: Bake\ne2: \"Bake\" significa \"cuocere al forno\" in italiano, non \"friggere\".\nc3: Fry\ne3: Correct! \"Fry\" significa \"friggere\" in italiano.\nc4: Grill\ne4: \"Grill\" significa \"grigliare\" in italiano, non \"friggere\".\na: 3\nw: 2\nq: How do you say \"mescolare\" (to stir) in English?\nc1: Mix\ne1: \"Mix\" significa \"miscelare\" o \"mescolare\" in italiano, ma è meno specifico di \"stir\".\nc2: Blend\ne2: \"Blend\" significa \"frullare\" o \"mescolare\" in italiano, di solito riferendosi a ingredienti liquidi o morbidi.\nc3: Stir\ne3: Correct! \"Stir\" significa \"mescolare\" in italiano.\nc4: Beat\ne4: \"Beat\" significa \"sbattere\" in italiano, non \"mescolare\".\na: 3\nw: 2\nq: What is the English translation for \"pentola\" (pot)?\nc1: Pan\ne1: \"Pan\" significa \"padella\" o \"tegame\" in italiano, non \"pentola\".\nc2: Pot\ne2: Correct! \"Pot\" significa \"pentola\" in italiano.\nc3: Kettle\ne3: \"Kettle\" significa \"bollitore\" in italiano, utilizzato per riscaldare l'acqua, non per cucinare.\nc4: Bowl\ne4: \"Bowl\" significa \"ciotola\" in italiano, non \"pentola\".\na: 2\nw: 3\nq: Translate \"affettare\" (to slice) to English.\nc1: Cut\ne1: \"Cut\" significa \"tagliare\" in italiano, che è più generico di \"affettare\".\nc2: Chop\ne2: \"Chop\" significa \"tritare\" o \"sminuzzare\" in italiano, non \"affettare\".\nc3: Slice\ne3: Correct! \"Slice\" significa \"affettare\" in italiano.\nc4: Dice\ne4: \"Dice\" significa \"tagliare a dadini\" in italiano, non \"affettare\".\na: 3\nw: 2\nq: How would you say \"grattugiare\" (to grate) in English?\nc1: Grind\ne1: \"Grind\" significa \"macinare\" in italiano, non \"grattugiare\".\nc2: Shred\ne2: \"Shred\" significa \"sminuzzare\" o \"grattugiare\" in italiano, ma di solito si riferisce a ingredienti come il formaggio o il cavolo.\nc3: Mince\ne3: \"Mince\" significa \"tritare finemente\" in italiano, non \"grattugiare\".\nc4: Grate\ne4: Correct! \"Grate\" significa \"grattugiare\" in italiano.\na: 4\nw: 2",
    f"input: Generate a quiz titled \"{request.data['title']}\" for {home_language} speakers learning {request.data['language']}. Passing score must be an integer not a percent, same with the time just an integer amount of minutes follow the examples given exactly in that format",
    "output: ",
    ]

    response = await model.generate_content_async(prompt_parts)

    generated_text = response.text.strip()

    quiz_data = parse_generated_questions(generated_text)

    quiz = await Quiz.objects.acreate(
        user=request.auth,
        title=quiz_data.get("title"),
        duration=quiz_data.get("duration"),
        passing_score=quiz_data.get("passing_score"),
        language_id=payload.language_id,
    )

    questions_data = quiz_data.get("questions", [])
    for question_data in questions_data:
        question_data["quiz"] = quiz.id
        serializer = QuestionSchema(**question_data)
        await Question.objects.acreate(**serializer.dict())

    return quiz


#Get list of quizzes
@router.get("/", response={200: [QuizSchema], codes_4xx: None}, auth=AuthBearer())
async def get_quizzes(request):
    return [quizz async for quizz in Quiz.objects.all()]



@router.post("/{quiz_id}/attempt", response={200: AttemptSchema, codes_4xx: None}, auth=AuthBearer())
async def submit_quiz_attempt(request, quiz_id: int, user_answers: dict):
    quiz = await Quiz.objects.aget(id=quiz_id)
    total_score = 0
    max_score = 0
    result = []

    async for question in Question.objects.filter(quiz=quiz).all():
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
    attempt = await Attempt.objects.acreate(user=request.auth, quiz=quiz, score=score)

    return {
        'attempt': AttemptSchema.from_orm(attempt).dict(),
        'result': result,
    }
import json
from rest_framework import generics, status
from rest_framework.response import Response
from languages.models import Language
from quizzes.models import Quiz
from quizzes.serializers import QuestionSerializer
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from django.conf import settings
import google.generativeai as genai
from rest_framework.permissions import IsAuthenticated
from analytics.models import UserAnalytics

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        language_id = self.request.data.get('language', {}).get('id')
        title = self.request.data.get('title')
        serializer.save(user=self.request.user, language_id=language_id, title=title)
class MessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
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
    def extract_topic_scores(self, text):
        print(text)
        topic_scores = json.loads(text.strip().replace("'", "\""))
        print(topic_scores)
        return topic_scores

    def get_queryset(self):
        conversation_id = self.kwargs["conversation_id"]
        return Message.objects.filter(conversation_id=conversation_id)

    def create(self, request, *args, **kwargs):
        conversation_id = self.kwargs["conversation_id"]
        conversation = Conversation.objects.get(id=conversation_id)
        user_message = request.data["content"]

        user_message_serializer = MessageSerializer(
            data={
                "conversation": conversation_id,
                "sender": "user",
                "content": user_message,
            }
        )
        user_message_serializer.is_valid(raise_exception=True)
        user_message_serializer.save()

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

        model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

        conversation_messages = Message.objects.filter(
            conversation=conversation
        ).order_by("timestamp")
        conversation_history = "\n".join(
            [
                f"{message.sender}: {message.content}"
                for message in conversation_messages
            ]
        )
        home_language = (
            request.user.home_language.name if request.user.home_language else "English"
        )
        learning_language = conversation.language.name
        prompt_parts = [
            f"You are a teacher of the {learning_language} language. Reply in {home_language} and provide examples when teaching. Be supportive and helpful.",
            "Unless specified, generate 5 example questions.",
            f"For newline characters inside table cells, use the special character sequence \"\\n\".",
            f"You are a teacher and master in the {learning_language} language. Use only markdown for outputting, including tables. For tables, use the following markdown rendering:",
            "\n| Syntax      | Description |\n| ----------- | ----------- |\n| Header      | Title       |\n| Paragraph   | Text        |",
            "Your role is to teach and provide explanations without directing to outside sources. Provide your responses in markdown format.",
            f"If the user asks for a quiz, FIRST add ___quiz!!!___ then generate a quiz with the following strict format:",
            "Here's an example of a generated quiz you must follwo this exact format:",
            "___quiz!!!___",
            "Quiz Title: Cooking Vocabulary\nDuration: 10\nPassing Score: 80\nq: What is the English word for \"friggere\" (to fry)?\nc1: Boil\ne1: \"Boil\" significa \"bollire\" in italiano, non \"friggere\".\nc2: Bake\ne2: \"Bake\" significa \"cuocere al forno\" in italiano, non \"friggere\".\nc3: Fry\ne3: Correct! \"Fry\" significa \"friggere\" in italiano.\nc4: Grill\ne4: \"Grill\" significa \"grigliare\" in italiano, non \"friggere\".\na: 3\nw: 2\nq: How do you say \"mescolare\" (to stir) in English?\nc1: Mix\ne1: \"Mix\" significa \"miscelare\" o \"mescolare\" in italiano, ma è meno specifico di \"stir\".\nc2: Blend\ne2: \"Blend\" significa \"frullare\" o \"mescolare\" in italiano, di solito riferendosi a ingredienti liquidi o morbidi.\nc3: Stir\ne3: Correct! \"Stir\" significa \"mescolare\" in italiano.\nc4: Beat\ne4: \"Beat\" significa \"sbattere\" in italiano, non \"mescolare\".\na: 3\nw: 2\nq: What is the English translation for \"pentola\" (pot)?\nc1: Pan\ne1: \"Pan\" significa \"padella\" o \"tegame\" in italiano, non \"pentola\".\nc2: Pot\ne2: Correct! \"Pot\" significa \"pentola\" in italiano.\nc3: Kettle\ne3: \"Kettle\" significa \"bollitore\" in italiano, utilizzato per riscaldare l'acqua, non per cucinare.\nc4: Bowl\ne4: \"Bowl\" significa \"ciotola\" in italiano, non \"pentola\".\na: 2\nw: 3\nq: Translate \"affettare\" (to slice) to English.\nc1: Cut\ne1: \"Cut\" significa \"tagliare\" in italiano, che è più generico di \"affettare\".\nc2: Chop\ne2: \"Chop\" significa \"tritare\" o \"sminuzzare\" in italiano, non \"affettare\".\nc3: Slice\ne3: Correct! \"Slice\" significa \"affettare\" in italiano.\nc4: Dice\ne4: \"Dice\" significa \"tagliare a dadini\" in italiano, non \"affettare\".\na: 3\nw: 2\nq: How would you say \"grattugiare\" (to grate) in English?\nc1: Grind\ne1: \"Grind\" significa \"macinare\" in italiano, non \"grattugiare\".\nc2: Shred\ne2: \"Shred\" significa \"sminuzzare\" o \"grattugiare\" in italiano, ma di solito si riferisce a ingredienti come il formaggio o il cavolo.\nc3: Mince\ne3: \"Mince\" significa \"tritare finemente\" in italiano, non \"grattugiare\".\nc4: Grate\ne4: Correct! \"Grate\" significa \"grattugiare\" in italiano.\na: 4\nw: 2",
            "At the end of each message, add a dictionary with the topic scores for the message, explaining what subjects you taught during this interaction. For example:",
            "!!!TOPICS!!!: {'subjunctive': 0.1, 'travel vocab': 0.3, 'past perfect': 0.6}",
            "Make sure to include the entire dictionary with the topic scores at the end of each message, in the format of the example. It should be the last lines of the message. Begin the dictionary with !!!TOPICS!!!: and then the dictionary in the format shown.",
            f"Conversation history:\n{conversation_history}",
            f"User: {user_message}",
            "AI Teacher:",
        ]
        prompt = "\n".join(prompt_parts)

        response = model.generate_content(prompt)
        topics = response.text[response.text.find("!!!TOPICS!!!") + 13 :]
        response = response.text[: response.text.find("!!!TOPICS!!!")]

        bot_response = response.replace("\n", "\\n")
        print(bot_response)
        if "___quiz!!!___" in response:
            quiz_data = self.parse_generated_questions(response[response.find("___quiz!!!___") + 13 :])
            quiz = Quiz.objects.create(
                language=conversation.language,
                user=request.user,
                title=quiz_data["title"],
                duration=quiz_data["duration"],
                passing_score=quiz_data["passing_score"],
            )
            questions_data = quiz_data["questions"]
            for question_data in questions_data:
                question_data["quiz"] = quiz.id
                serializer = QuestionSerializer(data=question_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

            # Generate a user-friendly response for quiz creation
            bot_response = f"Quiz created successfully! You can start the quiz at /quizzes/{quiz.id}/"
        else:
            bot_response = response.replace("\n", "\\n")

        # Logic to save the bot's response and return it
        bot_message_serializer = MessageSerializer(
            data={
                "conversation": conversation_id,
                "sender": "bot",
                "content": bot_response,
            }
        )
        bot_message_serializer.is_valid(raise_exception=True)
        bot_message_serializer.save()

        return Response(bot_message_serializer.data, status=status.HTTP_201_CREATED)
    
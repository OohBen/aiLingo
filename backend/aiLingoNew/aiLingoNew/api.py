from ninja import NinjaAPI
from users.api import router as users_router
from languages.api import router as languages_router
# from lessons.api import router as lessons_router
from quizzes.api import router as quizzes_router
# from analytics.api import router as analytics_router
from chat.api import router as chat_router

api = NinjaAPI()
api.add_router('/users/', users_router)
api.add_router('/languages/', languages_router)
# api.add_router('/lessons/', lessons_router)
api.add_router('/quizzes/', quizzes_router)
# api.add_router('/analytics/', analytics_router)
api.add_router('/chat/', chat_router)
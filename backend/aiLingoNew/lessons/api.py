from ninja import Router
from .models import Lesson, UserLesson
from .schemas import LessonSchema, UserLessonSchema

router = Router()

@router.get('/', response=List[LessonSchema])
async def list_lessons(request):
    return await Lesson.objects.all()

@router.get('/{lesson_id}', response=LessonSchema)
async def get_lesson(request, lesson_id: int):
    return await Lesson.objects.aget(id=lesson_id)

@router.post('/', response=LessonSchema)
async def create_lesson(request, payload: LessonSchema):
    lesson = await Lesson.objects.acreate(**payload.dict())
    return lesson

@router.put('/{lesson_id}', response=LessonSchema)
async def update_lesson(request, lesson_id: int, payload: LessonSchema):
    lesson = await Lesson.objects.aget(id=lesson_id)
    for attr, value in payload.dict().items():
        setattr(lesson, attr, value)
    await lesson.asave()
    return lesson

@router.delete('/{lesson_id}')
async def delete_lesson(request, lesson_id: int):
    await Lesson.objects.aget(id=lesson_id).adelete()
    return 204, None

@router.get('/user-lessons', response=List[UserLessonSchema], auth=AuthBearer())
async def list_user_lessons(request):
    return await UserLesson.objects.filter(user=request.auth).all()

@router.post('/user-lessons', response=UserLessonSchema, auth=AuthBearer())
async def create_user_lesson(request, payload: UserLessonSchema):
    user_lesson = await UserLesson.objects.acreate(user=request.auth, **payload.dict())
    return user_lesson

@router.put('/user-lessons/{user_lesson_id}', response=UserLessonSchema, auth=AuthBearer())
async def update_user_lesson(request, user_lesson_id: int, payload: UserLessonSchema):
    user_lesson = await UserLesson.objects.aget(id=user_lesson_id, user=request.auth)
    for attr, value in payload.dict().items():
        setattr(user_lesson, attr, value)
    await user_lesson.asave()
    return user_lesson

@router.delete('/user-lessons/{user_lesson_id}', auth=AuthBearer())
async def delete_user_lesson(request, user_lesson_id: int):
    await UserLesson.objects.aget(id=user_lesson_id, user=request.auth).adelete()
    return 204, None
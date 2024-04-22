from ninja import Router
from .models import User
from .schemas import UserSchema, UserRegistrationSchema, TokenSchema
from django.contrib.auth import authenticate
from ninja.security import HttpBearer

router = Router()

class AuthBearer(HttpBearer):
    async def authenticate(self, request, token):
        try:
            return await User.objects.aget(token=token)
        except User.DoesNotExist:
            return None

@router.post('/register', response=UserSchema)
async def register(request, payload: UserRegistrationSchema):
    user = await User.objects.acreate_user(**payload.dict())
    return user

@router.post('/login', response=TokenSchema)
async def login(request, email: str, password: str):
    user = await authenticate(request, email=email, password=password)
    if user:
        return {'token': user.token}
    else:
        return 401, {'message': 'Invalid credentials'}

@router.get('/me', response=UserSchema, auth=AuthBearer())
async def get_me(request):
    return request.auth

@router.patch('/me', response=UserSchema, auth=AuthBearer())
async def update_me(request, payload: UserSchema):
    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(request.auth, attr, value)
    await request.auth.asave()
    return request.auth
from typing import List
from ninja import Router
from .models import Language
from .schemas import LanguageSchema

router = Router()

@router.get('/', response=List[LanguageSchema])
async def list_languages(request):
    return await Language.objects.all()

@router.get('/{language_id}', response=LanguageSchema)
async def get_language(request, language_id: int):
    return await Language.objects.aget(id=language_id)

@router.post('/', response=LanguageSchema)
async def create_language(request, payload: LanguageSchema):
    language = await Language.objects.acreate(**payload.dict())
    return language

@router.put('/{language_id}', response=LanguageSchema)
async def update_language(request, language_id: int, payload: LanguageSchema):
    language = await Language.objects.aget(id=language_id)
    for attr, value in payload.dict().items():
        setattr(language, attr, value)
    await language.asave()
    return language

@router.delete('/{language_id}')
async def delete_language(request, language_id: int):
    await Language.objects.aget(id=language_id).adelete()
    return 204, None
from ninja import Schema

class LanguageSchema(Schema):
    id: int
    code: str
    name: str
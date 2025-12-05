from fastapi import APIRouter
from app.core.security import create_token
from pydantic import BaseModel

router = APIRouter()

class AuthInput(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(auth: AuthInput):
    if (auth.username == 'admin') and (auth.password == 'admin'):
        token = create_token({'sub': auth.username})
        return {'token_access': token}
    return {'error': "Invalid Credentials."}
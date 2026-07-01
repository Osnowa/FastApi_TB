from fastapi import APIRouter, HTTPException, status

from app.database import SessionDep
from app.schemas.users import SUserRegister, SUserLogin, SUserOut, SToken
from app.auth.service import hash_password, verify_password, create_access_token

from app.repository import Repository

router = APIRouter(prefix="/auth", tags=["Авторизация"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: SUserRegister, session: SessionDep) -> SUserOut:
    '''ручка для регистрации пользователя, отдаем пользователя без пароля, пароль хешируем'''
    repo = Repository(session)
    execute = await repo.get_user(user_data.email)
    if execute:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
            )
    
    user_data.password = hash_password(user_data.password)
    user = await repo.add_user(user_data)
    return user

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(user_data: SUserLogin, session: SessionDep) -> SToken:
    '''ручка для логина пользователя (по email, пароль), отдаем токен'''
    repo = Repository(session)
    user = await repo.get_user(user_data.email) 
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Невалидные учетные данные"
            )
    
    # Создаем и возвращаем токен (токен хранится в заголовке)
    access_token = create_access_token({"sub": str(user.id)})
    return SToken(access_token=access_token)
    
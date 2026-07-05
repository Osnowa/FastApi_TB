from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.services.api_client import api_client  # 👈 Импортируем глобальный
from app.auth.service import ACCESS_TOKEN_EXPIRE_MINUTES
import httpx

from bot.states.redis import r
import logging

from bot.states.register_auth import FSMAddRegister, FSMAddLogin


logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('register'))
async def register(message: Message, state: FSMContext):
    '''Начало регистрации'''
    await message.answer('Добрый день ! Для регистрации, пожалуйста, введите Вашу почту ...')
    await state.set_state(FSMAddRegister.email)

@router.message(StateFilter(FSMAddRegister.email))
async def register_email(message: Message, state: FSMContext):
    '''Регистрация (ввод пароля)'''
    # Сохраняем почту
    await state.update_data(email=message.text)
    await message.answer('Введите пароль ...')
    await state.set_state(FSMAddRegister.password)

@router.message(StateFilter(FSMAddRegister.password))
async def register_password(message: Message, state: FSMContext):
    '''Регистрация (окончание)'''
    # Сохраняем пароль
    await state.update_data(password=message.text)
    # Получаем почту и пароль пользователя
    data = await state.get_data()
    # Регистрируем пользователя в системе
    try:
        result = await api_client.register(data['email'], data['password'])
    except httpx.HTTPError as e:
        if e.response.status_code == 400:
            logger.exception(f"Пользователь с почтой {data['email']} уже зарегистрирован")
            await message.answer(f"Пользователь с почтой {data['email']} уже зарегистрирован")
            return
        await message.answer(f"Произошла ошибка: {e}")
        logger.exception(f"Произошла ошибка: {e}")
        return
    await message.answer(f"Пользователь {result['email']} зарегистрирован =)\n"
                         "Вы автоматически вошли в систему.")
    await state.clear()

    # Выдаем токен пользователю
    try:
        response = await api_client.login(data['email'], data['password'])
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.exception(f"Произошла ошибка: {e}")
        return
    # сохраняем токен в redis
    await r.hset(f"token:{message.from_user.id}", mapping={"token": response['access_token']})
    await r.expire(f"token:{message.from_user.id}", ACCESS_TOKEN_EXPIRE_MINUTES * 60) # Выдаем время жизни токена


@router.message(Command('login'))
async def login(message: Message, state: FSMContext):
    '''Вход в систему'''
    token = await r.ttl(f"token:{message.from_user.id}")
    if token > 0:
        await message.answer("Вы уже авторизованы ! Доступ к командам бота открыт !")
        return
    await message.answer('Добрый день ! Для входа, пожалуйста, введите Вашу почту ...')
    await state.set_state(FSMAddLogin.email)

@router.message(StateFilter(FSMAddLogin.email))
async def login_email(message: Message, state: FSMContext):
    '''Вход в систему (ввод пароля)'''
    # Сохраняем почту
    await state.update_data(email=message.text)
    await message.answer('Введите пароль ...')
    await state.set_state(FSMAddLogin.password)

@router.message(StateFilter(FSMAddLogin.password))
async def login_password(message: Message, state: FSMContext):
    '''Вход в систему (окончание)'''
    # Сохраняем пароль
    await state.update_data(password=message.text)
    # Получаем почту и пароль пользователя
    data = await state.get_data()
    # Регистрируем пользователя в системе
    try:
        response = await api_client.login(data['email'], data['password'])
    except httpx.HTTPError as e:
        await message.answer(f"Произошла ошибка: {e}")
        logger.exception(f"Произошла ошибка: {e}")
        return 
    
    await state.clear()
    logger.info(
    "Пользователь %s успешно авторизовался",
    data["email"]
    )
    # сохраняем токен в redis
    await r.hset(f"token:{message.from_user.id}", mapping={"token": response['access_token']})
    await r.expire(f"token:{message.from_user.id}", ACCESS_TOKEN_EXPIRE_MINUTES * 60) # Выдаем время жизни токена

    await message.answer(f"Вы успешно авторизировались !"
                         "Доступ к командам бота открыт !")
    

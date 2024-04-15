"""CRUD операции с базой данных."""
import uuid
from typing import Optional, Tuple

from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.future import select

from wav_to_mp3.database.database import async_session
from wav_to_mp3.database.models import Audio, User
from wav_to_mp3.utils.enums import Result


async def create_user(username: str) -> Tuple[Result, Optional[User]]:
    """
    Создание нового пользователя в БД.

    Args:
        username (str): имя пользователя.

    Returns:
        Tuple[Result, User]
    """

    async with async_session() as session:

        new_user = User(
            id=uuid.uuid5(uuid.NAMESPACE_X500, username),
            name=username,
            access_token=uuid.uuid4(),
        )

        session.add(new_user)

        try:
            await session.commit()
        except IntegrityError:
            return Result.NameExists, None
        except DBAPIError:
            return Result.NameTooLong, None

        return Result.Success, new_user


async def get_user_by_id_and_access_token(
        user_id: str,
        access_token: str,
) -> Optional[User]:
    """
    Получение пользователя из БД по id и access_token.

    Args:
         user_id (str): ID пользователя
         access_token(str): access_token пользователя

    Returns:
         User или None
    """

    async with async_session() as session:
        async with session.begin():
            query = await session.execute(
                select(User)
                .where(
                    User.id == user_id and User.access_token == access_token
                )
            )
            return query.scalar()


async def create_audio(file: bytes, filename: str, user: User) -> str:
    """
    Создание нового Аудио в БД.

    Args:
        file (bytes): аудиофайл
        filename (str): имя аудиофайла
        user (User): пользователь-владелец аудиофайла

    Returns:
        str: ID аудиозаписи
    """
    async with async_session() as session:
        new_audio = Audio(
            user=user,
            id=uuid.uuid4(),
            name=filename,
            file=file,
        )
        session.add(new_audio)
        await session.commit()

        return str(new_audio.id)


async def get_audio(audio_id: str, user_id: str) -> Optional[Audio]:
    """
    Получение аудиофайла из БД.

    Args:
         audio_id (str):
         user_id (str):

    Returns:
        Audio или None
    """
    async with async_session() as session:
        async with session.begin():
            query = await session.execute(
                select(Audio)
                .where(
                    Audio.id == audio_id and Audio.user_id == user_id
                )
            )
            return query.scalar()

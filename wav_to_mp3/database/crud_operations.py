"""CRUD операции с базой данных."""
import uuid
from typing import Optional, Tuple

from sqlalchemy.exc import DBAPIError, IntegrityError

from wav_to_mp3.database.database import async_session
from wav_to_mp3.database.models import Audio, User
from wav_to_mp3.utils.enums import Result


async def create_user(username: str) -> Tuple[Result, Optional[User]]:
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

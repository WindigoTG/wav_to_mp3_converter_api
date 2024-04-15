""" Эндпоинты для работы с аудиозаписями. """
import io
import os

from fastapi import APIRouter, Depends, File, Header, UploadFile, status, Query
from fastapi.responses import StreamingResponse
from typing_extensions import Annotated

from wav_to_mp3.converter.converter import convert_wav_to_mp3
from wav_to_mp3.database import crud_operations
from wav_to_mp3.utils import schemas, standart_responses
from wav_to_mp3.utils.enums import Tags
from wav_to_mp3.utils.validators import (
    AllowedExtensions,
    LimitedSize,
    validated,
)

DEFAULT_SIZE = 1024
file_size_limit = os.getenv("FILE_SIZE_LIMIT")

try:
    file_size_limit = int(file_size_limit)
except ValueError:
    file_size_limit = DEFAULT_SIZE

router = APIRouter()


@router.post(
    "/api/audio",
    responses={status.HTTP_400_BAD_REQUEST: {"model": schemas.FailResponse}},
    status_code=status.HTTP_201_CREATED,
    tags=[Tags.audio],
)
async def upload_audio(
    user_id: Annotated[str, Header()],
    access_token: Annotated[str, Header()],
    audio: Annotated[UploadFile, Depends(
        validated(
            File(),
            AllowedExtensions("wav"),
            LimitedSize(file_size_limit),
        )
    )],
):
    """
    Загрузка аудиофайла.

    Args:
        user_id: ID пользователя
        access_token: access_token пользователя
        audio: аудиофайл.
    Returns:
        audio_id, download_url
    """
    user = await crud_operations.get_user_by_id_and_access_token(
        user_id,
        access_token,
    )

    if not user:
        return standart_responses.get_bad_request_response(
            "Invalid user_id or access_token"
        )

    mp3_audio = convert_wav_to_mp3(audio.file.read())

    if not mp3_audio:
        return standart_responses.get_bad_request_response(
            "Unable to convert file to mp3"
        )

    audio_id = await crud_operations.create_audio(
        mp3_audio,
        audio.filename.replace('.wav', '.mp3'),
        user,
    )

    return standart_responses.get_audio_created_response(audio_id, user_id)


@router.get(
    "/api/audio",
    responses={status.HTTP_404_NOT_FOUND: {"model": schemas.FailResponse}},
    response_class=StreamingResponse,
    response_model=schemas.AudioUploadedResponse,
    status_code=status.HTTP_200_OK,
    tags=[Tags.audio],
)
async def get_audio(
    id: Annotated[str, Query()],
    user: Annotated[str, Query()],
):
    """
    Получение аудиофайла для скачивания.

    Args:
        id (str): id аудиофайла
        user: (str): id пользователя, загрузившего файл
    Returns:
        Запрошенный файл или сообщение об ошибке.
    """
    audio = await crud_operations.get_audio(id, user)

    if not audio:
        return standart_responses.get_not_found_response(
            "Invalid ID or user"
        )

    return StreamingResponse(
        io.BytesIO(audio.file),
        media_type="audio/mp3",
        headers={
            "content-disposition": f"attachment; filename={audio.name}",
            "content-length": str(len(audio.file)),
        }
    )

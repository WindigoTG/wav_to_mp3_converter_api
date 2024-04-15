""" Набор готовых стандартных JSONResponse. """
import os

from fastapi import status
from fastapi.responses import JSONResponse

from wav_to_mp3.database.models import User
from wav_to_mp3.utils.enums import Result


domain = os.getenv('BASE_DOMAIN', "http://127.0.0.1:5000")


def get_bad_request_response(message: str) -> JSONResponse:
    """
        Получить готовый Bad Request ответ c сообщением об ошибке.

        Args:
            message (str): сообщение об ошибке.

        Returns:
            JSONResponse
        """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_message": message,
        }
    )


def get_not_found_response(message: str) -> JSONResponse:
    """
        Получить готовый Not Found ответ c сообщением об ошибке.

        Args:
            message (str): сообщение об ошибке.

        Returns:
            JSONResponse
        """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_message": message,
        }
    )


def get_response_for_result(result: Result) -> JSONResponse:
    """
    Получить готовый ответ для указанного CRUD результата.

    Args:
        result (Result): Enum результат CRUD операции.

    Returns:
        JSONResponse
    """

    if result == Result.NameExists:
        return get_bad_request_response(
            "User with provided name already exists"
        )

    if result == Result.NameTooLong:
        return get_bad_request_response(
            "Name must be at most 30 characters long"
        )

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT
    )


def get_user_created_response(user: User) -> JSONResponse:
    """
    Получить готовый ответ об успешном создании пользователя.

    Args:
        user (User): созданный пользователь.

    Returns:
        JSONResponse
    """

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "username": user.name,
            "user_id": str(user.id),
            "access_token": str(user.access_token),
        }
    )


def get_audio_created_response(audio_id: str, user_id: str) -> JSONResponse:
    """
    Получить готовый ответ об успешной загрузке аудиофайла.

    Args:
         audio_id (str): ID аудиофайла
         user_id (str): ID пользователя, загрузившего файл
    Returns:
        JSONResponse
    """

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "audio_id": audio_id,
            "download_url": f"{domain}/api/audio?id={audio_id}&user={user_id}"
        }
    )
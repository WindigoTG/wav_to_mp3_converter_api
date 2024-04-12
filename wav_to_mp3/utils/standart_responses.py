""" Набор готовых стандартных JSONResponse. """

from fastapi import status
from fastapi.responses import JSONResponse

from wav_to_mp3.database.models import User
from wav_to_mp3.utils.enums import Result


def get_response_for_result(result: Result):
    """
    Получить готовый ответ для указанного CRUD результата.

    Args:
        result (Result): Enum результат CRUD операции.

    Returns:
        JSONResponse
    """

    if result == Result.NameExists:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_message": "User with provided name already exists",
            }
        )

    if result == Result.NameTooLong:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "error_message": "Name must be at most 30 characters long",
            }
        )

    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT
    )


def get_user_created_response(user: User):
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "username": user.name,
            "user_id": str(user.id),
            "access_token": str(user.access_token),
        }
    )

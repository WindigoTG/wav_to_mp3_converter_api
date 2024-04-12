""" Эндпоинты для работы с пользователями. """

from fastapi import APIRouter, status, Header
from typing_extensions import Annotated

from wav_to_mp3.database import crud_operations
from wav_to_mp3.utils import schemas, standart_responses
from wav_to_mp3.utils.enums import Result, Tags

router = APIRouter()


@router.post(
    "/api/users",
    responses={status.HTTP_400_BAD_REQUEST: {"model": schemas.FailResponse}},
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создание нового пользователя",
    tags=[Tags.users],
)
async def create_user(
  username: Annotated[str, Header()]
):
    result, user = await crud_operations.create_user(username)

    if result == Result.Success:
        return standart_responses.get_user_created_response(user)

    return standart_responses.get_response_for_result(result)

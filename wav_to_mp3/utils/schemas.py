"""Pydantic схемы для верификации данных."""

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """ Модель ответа с данными пользователя. """

    model_config = ConfigDict(from_attributes=True)

    username: str
    user_id: str
    access_token: str


class FailResponse(BaseModel):
    """Модель неудачного ответа."""

    error_message: str

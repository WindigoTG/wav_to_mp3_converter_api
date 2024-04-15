"""Pydantic схемы для верификации данных."""

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """ Модель ответа с данными пользователя. """

    model_config = ConfigDict(from_attributes=True)

    username: str
    user_id: str
    access_token: str


class AudioUploadedResponse(BaseModel):
    """ Модель ответа с данными успешно загруженного аудиофайла. """

    model_config = ConfigDict(from_attributes=True)

    audio_id: str
    download_url: str


class FailResponse(BaseModel):
    """Модель неудачного ответа."""

    error_message: str

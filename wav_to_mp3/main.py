""" Точка входа в приложение. """

from fastapi import FastAPI

from wav_to_mp3.database import database
from wav_to_mp3.endpoints import audio, users

app = FastAPI()
app.include_router(audio.router)
app.include_router(users.router)


@app.on_event("startup")
async def startup() -> None:
    """ Первоначальная настройка перед запуском приложения. """
    await database.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """ Завершение работы приложения. """
    await database.shutdown_db()

""" Точка входа в приложение. """

from fastapi import FastAPI

from vaw_to_mp3.database import database

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    """ Первоначальная настройка перед запуском приложения. """
    await database.init_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    """ Завершение работы приложения. """
    await database.shutdown_db()

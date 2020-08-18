from typing import Callable

from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from config import DATABASE_URL


async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to {0}", repr(DATABASE_URL))

    register_tortoise(
        app,
        db_url=str(DATABASE_URL),
        modules={"models": ["models"], "aerich.models": ["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")


def create_start_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app)

    return start_app


def create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    @logger.catch
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app

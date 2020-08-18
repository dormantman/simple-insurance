from fastapi import FastAPI
from loguru import logger
from tortoise.contrib.fastapi import register_tortoise

from core.config import DATABASE_URL


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
    logger.info("Closing connection to db")

    await app.state.pool.close()

    logger.info("Connection closed")

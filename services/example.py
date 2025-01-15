from sqlalchemy.ext.asyncio import AsyncSession
from module.cookie import CookieBase
from module.example import User
from services.db import get_session
from loguru import logger

class ExampleService:
    @classmethod
    async def cookie_add(cls, cookie: CookieBase):
        logger.info(f"base add tuple begin")
        try:
            instance = CookieBase.model_validate(cookie)
            async for session in get_session():
                async with session.begin():
                    session.add(cookie)
                    await session.flush()
                    logger.info(f"Cookie added successfully.")
            logger.info(f"base add tuple end")
            return cookie
        except Exception as e:
            logger.error(f"Error adding cookie: {e}")
            raise

    @classmethod
    async def user_add(cls, user: User):
        logger.info(f"base add tuple begin")
        try:
            instance = User.model_validate(user)
            async for session in get_session():
                async with session.begin():
                    session.add(user)
                    logger.info(f"Cookie added successfully.")
            logger.info(f"base add tuple end")
            return user
        except Exception as e:
            logger.error(f"Error adding cookie: {e}")
            raise

import json
from os import getenv

from dto import RedisSetexRequestDTO, SessionDTO
from models import Session
from repositories.base.base_repository import BaseRepository
from repositories.base.redis_client import RedisClient
from utils import CryptographyUtils


class SessionRepository(BaseRepository):
    model = Session

    async def create_session(self, user_id: int, token: str, headers: dict) -> None:
        redis_client = RedisClient.get_instance()

        session = self.model(
            user_id=user_id,
            token=CryptographyUtils.generate_fingerprint(token),
            host=headers.get("host"),
            user_agent=headers.get("user-agent"),
        )

        await self.create(session)

        key = redis_client.create_key("session", session.user_id)
        stringified_session = json.dumps(session.model_dump(), default=str)

        data = RedisSetexRequestDTO(name=key, time=getenv("TOKEN_TTL"), value=stringified_session)

        await redis_client.setex(**data.model_dump())

    async def get_session(self, user_id: int) -> SessionDTO | None:
        redis_client = RedisClient.get_instance()
        key = redis_client.create_key("session", user_id)
        stringified_session = await redis_client.get(key)

        if not stringified_session:
            return None

        return SessionDTO(**json.loads(stringified_session))

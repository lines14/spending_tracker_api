import json
from os import getenv
from models import Session
from typing import Optional
from utils import CryptographyUtils
from dto import RedisSetexRequestDTO, SessionDTO
from repositories.base.redis_client import RedisClient
from repositories.base.base_repository import BaseRepository

class SessionRepository(BaseRepository):    
    def __init__(self):
        super().__init__(model=Session)

    async def create_session(self, user_id: int, token: str, headers: dict) -> None:
        redis_client = RedisClient()

        hashed_token = CryptographyUtils.hash_string(token)

        session = self.model(
            user_id=user_id, 
            token=hashed_token,
            host=headers.get('host'),
            user_agent=headers.get('user-agent')
        )

        await self.create(session)

        name = redis_client.create_key('session', session.user_id)
        stringified_session = json.dumps(session.model_dump(), default=str)

        data = RedisSetexRequestDTO(
            name=name,
            time=getenv('TOKEN_TTL'), 
            value=stringified_session
        )

        await redis_client.setex(**data.model_dump())

    async def get_session(self, user_id: int) -> Optional[SessionDTO]:
        redis_client = RedisClient()
        name = redis_client.create_key('session', user_id)
        stringified_session = await redis_client.get(name)

        if not stringified_session:
            return None

        return SessionDTO(**json.loads(stringified_session))
    
    async def delete_session(self, user_id: int) -> None:
        redis_client = RedisClient()
        name = redis_client.create_key('session', user_id)
        await redis_client.delete(name)
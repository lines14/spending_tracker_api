from fastapi import Response
from utils import DataUtils, ResponseUtils

class GreetingsService:
    async def greetings(self) -> Response:
        return await ResponseUtils.success(DataUtils.responses.info_message)
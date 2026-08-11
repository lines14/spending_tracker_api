from fastapi import Response

from utils import DataUtils, ResponseUtils


class GreetingsController:
    @staticmethod
    async def greetings() -> Response:
        return await ResponseUtils.success(DataUtils.responses.info_message)

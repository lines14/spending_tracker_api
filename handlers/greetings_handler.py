from fastapi import Response
from utils.data_utils import DataUtils
from utils.response_utils import ResponseUtils

class GreetingsHandler:
    async def greetings(self) -> Response:
        return await ResponseUtils.success(DataUtils.responses.info_message)
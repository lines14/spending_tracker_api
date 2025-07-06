from fastapi import Response
from services import GreetingsService

class GreetingsController:
    async def greetings() -> Response:
        return await GreetingsService().greetings()
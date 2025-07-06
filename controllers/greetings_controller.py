from fastapi import Response
from services import GreetingsService

class GreetingsController:
    async def greetings() -> Response:
        greetings_service = GreetingsService()
        return await greetings_service.greetings()
import os
import sys
from models import Session
sys.path.append(os.getcwd())
from dotenv import load_dotenv

load_dotenv()

class SessionsCleanerSchedule:
    async def delete_expired_sessions(self) -> None:
        await Session().delete_all()
        print(f'INFO:     Successfully deleted expired sessions')
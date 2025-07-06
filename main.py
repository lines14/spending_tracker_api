import asyncio
import aioschedule
from routes import *
from os import getenv
from scheduler import *
from middlewares import *
from fastapi import FastAPI
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

sessions_cleaner_schedule = SessionsCleanerSchedule()
currency_rates_updater_schedule = CurrencyRatesUpdaterSchedule()

async def start_scheduler():
    (aioschedule.every().hour.at(":05")
     .do(sessions_cleaner_schedule.delete_expired_sessions))
    (aioschedule.every().hour.at(":10")
     .do(currency_rates_updater_schedule.update_currency_rates))
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(start_scheduler())
    yield

app = FastAPI(
    lifespan=lifespan,
    title='Spending tracker API',
    docs_url='/docs',
    redoc_url='/redoc',
    root_path='/api'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv('FRONT_URL')],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.add_middleware(AuthMiddleware)
app.add_middleware(LogErrorsMiddleware)
app.include_router(router)
app.include_router(purchase_router)
app.include_router(bank_account_router)
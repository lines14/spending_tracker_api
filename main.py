import asyncio
import aioschedule
from routes import *
from os import getenv
from scheduler import *
from middlewares import *
from fastapi import FastAPI
from dotenv import load_dotenv
from db.base.base_db import BaseDB
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

async def start_scheduler():    
    (aioschedule.every().hour.at(":10")
     .do(CurrencyRatesUpdaterSchedule().update_currency_rates))
    
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)
        
@asynccontextmanager
async def lifespan(app: FastAPI):
    await BaseDB().init_tables()
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
app.include_router(user_router)
app.include_router(purchase_router)
app.include_router(bank_account_router)
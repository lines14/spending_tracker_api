import asyncio
from contextlib import asynccontextmanager
from os import getenv

import aioschedule
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.base.base_db import BaseDB
from db.observers import init_observers
from middlewares import AuthMiddleware, LogErrorsMiddleware
from routes import bank_account_router, purchase_router, router, user_router
from scheduler import CurrencyRatesUpdaterSchedule

load_dotenv()

background_tasks = set()


async def start_scheduler():
    (aioschedule.every().hour.at(":10").do(CurrencyRatesUpdaterSchedule().update_currency_rates))

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_observers()
    await BaseDB().init_tables()
    task = asyncio.create_task(start_scheduler())
    background_tasks.add(task)
    task.add_done_callback(background_tasks.discard)

    yield

    await BaseDB.dispose_engine()


app = FastAPI(lifespan=lifespan, title="Spending tracker API", docs_url="/docs", redoc_url="/redoc", root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv("FRONT_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(AuthMiddleware)
app.add_middleware(LogErrorsMiddleware)
app.include_router(router)
app.include_router(user_router)
app.include_router(purchase_router)
app.include_router(bank_account_router)

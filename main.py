import asyncio
import aioschedule
from os import getenv
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from middlewares import AuthMiddleware, LogErrorsMiddleware
from scheduler.currency_rates_updater import CurrencyRatesUpdater
from DTO import UserDTO, ResponseContentDTO, PurchaseDTO, BankAccountDTO
from handlers import (AuthHandler, TemplateHandler, GreetingsHandler, 
                      RegistrationHandler, PurchaseHandler, BankAccountHandler)

load_dotenv()

auth_handler = AuthHandler()
template_handler = TemplateHandler()
purchase_handler = PurchaseHandler()
greetings_handler = GreetingsHandler()
bank_account_handler = BankAccountHandler()
registration_handler = RegistrationHandler()
currency_rates_updater = CurrencyRatesUpdater()

async def start_scheduler():
    aioschedule.every().hour.at(":10").do(currency_rates_updater.update)
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

@app.get("/", response_class=HTMLResponse)
async def template(request: Request) -> Response:
    return await template_handler.template(request)

@app.post('/registration', response_model=ResponseContentDTO)
async def registration(user: UserDTO) -> Response:
    return await registration_handler.registration(user)

@app.post('/auth', response_model=ResponseContentDTO)
async def auth(request: Request, user: UserDTO) -> Response:
    return await auth_handler.auth(request, user)

@app.get('/greetings', response_model=ResponseContentDTO)
async def greetings(request: Request) -> Response:
    return await greetings_handler.greetings()

@app.post('/purchase', response_model=ResponseContentDTO)
async def create_purchase(request: Request, purchase: PurchaseDTO) -> Response:
    return await purchase_handler.create_purchase(purchase)

@app.post('/bank_account', response_model=ResponseContentDTO)
async def create_bank_account(request: Request, bank_account: BankAccountDTO) -> Response:
    return await bank_account_handler.create_bank_account(bank_account)

@app.get('/bank_account/{id}', response_model=BankAccountDTO)
async def get_bank_account(request: Request, id: int) -> Response:
    return await bank_account_handler.get_bank_account(id)

@app.delete('/bank_account/{id}', response_model=ResponseContentDTO)
async def delete_bank_account(request: Request, id: int) -> Response:
    return await bank_account_handler.delete_bank_account(id)
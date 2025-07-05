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
from controllers import (AuthController, TemplateController, GreetingsController, 
                      UserController, PurchaseController, BankAccountController)

load_dotenv()

auth_controller = AuthController()
template_controller = TemplateController()
purchase_controller = PurchaseController()
greetings_controller = GreetingsController()
currency_rates_updater = CurrencyRatesUpdater()
bank_account_controller = BankAccountController()
user_controller = UserController()

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
    return await template_controller.get_template(request)

@app.post('/registration', response_model=ResponseContentDTO)
async def create_user(user: UserDTO) -> Response:
    return await user_controller.create_user(user)

@app.delete('/user/{id}', response_model=ResponseContentDTO)
async def delete_user(request: Request, id: int) -> Response:
    return await user_controller.delete_user(id)

@app.post('/auth', response_model=ResponseContentDTO)
async def auth(request: Request, user: UserDTO) -> Response:
    return await auth_controller.auth(request, user)

@app.get('/greetings', response_model=ResponseContentDTO)
async def greetings(request: Request) -> Response:
    return await greetings_controller.greetings()

@app.post('/purchase', response_model=ResponseContentDTO)
async def create_purchase(request: Request, purchase: PurchaseDTO) -> Response:
    return await purchase_controller.create_purchase(purchase)

@app.post('/bank_account', response_model=ResponseContentDTO)
async def create_bank_account(request: Request, bank_account: BankAccountDTO) -> Response:
    return await bank_account_controller.create_bank_account(bank_account)

@app.get('/bank_account/{id}', response_model=BankAccountDTO)
async def get_bank_account(request: Request, id: int) -> Response:
    return await bank_account_controller.get_bank_account(id)

@app.delete('/bank_account/{id}', response_model=ResponseContentDTO)
async def delete_bank_account(request: Request, id: int) -> Response:
    return await bank_account_controller.delete_bank_account(id)
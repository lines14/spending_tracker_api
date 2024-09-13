import asyncio
import aioschedule
from os import getenv
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from DTO import UserDTO, ResponseContentDTO
from handlers.auth_handler import AuthHandler
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from handlers.template_handler import TemplateHandler
from middlewares.auth_middleware import AuthMiddleware
from handlers.greetings_handler import GreetingsHandler
from handlers.registration_handler import RegistrationHandler
from scheduler.currency_rates_updater import CurrencyRatesUpdater

load_dotenv()

auth_handler = AuthHandler()
auth_middleware = AuthMiddleware()
template_handler = TemplateHandler()
greetings_handler = GreetingsHandler()
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

@app.get("/", response_class=HTMLResponse)
async def template(request: Request) -> Response:
    return await template_handler.template(request)

@app.post('/registration', response_model=ResponseContentDTO)
async def auth(user: UserDTO) -> Response:
    return await registration_handler.registration(user)

@app.post('/auth', response_model=ResponseContentDTO)
async def auth(request: Request, user: UserDTO) -> Response:
    return await auth_handler.auth(request, user)

@app.get('/greetings', response_model=ResponseContentDTO)
@auth_middleware.check_bearer_token
async def greetings(request: Request) -> Response:
    return await greetings_handler.greetings()
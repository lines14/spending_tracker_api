from controllers import *
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from DTO import ResponseContentDTO, BankAccountDTO

router = APIRouter()
router.get("/", response_class=HTMLResponse)(TemplateController.get_template)
router.get('/greetings', response_model=ResponseContentDTO)(GreetingsController.greetings)

router.post('/registration', response_model=ResponseContentDTO)(UserController.create_user)
router.post('/auth', response_model=ResponseContentDTO)(AuthController.auth)

user_router = APIRouter(prefix="/user", tags=["User"])
user_router.get('/{id}', response_model=ResponseContentDTO)(UserController.get_user)
user_router.delete('/{id}', response_model=ResponseContentDTO)(UserController.delete_user)

purchase_router = APIRouter(prefix="/purchase", tags=["Purchase"])
purchase_router.post('', response_model=ResponseContentDTO)(PurchaseController.create_purchase)

bank_account_router = APIRouter(prefix="/bank_account", tags=["Bank account"])
bank_account_router.post('', response_model=ResponseContentDTO)(BankAccountController.create_bank_account)
bank_account_router.get('/{id}', response_model=BankAccountDTO)(BankAccountController.get_bank_account)
bank_account_router.delete('/{id}', response_model=ResponseContentDTO)(BankAccountController.delete_bank_account)
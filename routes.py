from controllers import *
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from dto import ResponseContentDTO, BankAccountDTO, PurchaseDTO, UserDTO

router = APIRouter()
router.get("/", response_class=HTMLResponse)(TemplateController.get_template)
router.post('/auth', response_model=ResponseContentDTO)(AuthController.auth)
router.get('/greetings', response_model=ResponseContentDTO)(GreetingsController.greetings)
router.get('/clear-cache', response_model=ResponseContentDTO)(CacheController.clear_cache)

user_router = APIRouter(prefix="/user", tags=["User"])
router.post('/registration', response_model=UserDTO)(UserController.create_user)
user_router.get('/{id}', response_model=UserDTO)(UserController.get_user)
user_router.put('/{id}', response_model=UserDTO)(UserController.update_user)
user_router.delete('/{id}', response_model=ResponseContentDTO)(UserController.delete_user)

purchase_router = APIRouter(prefix="/purchase", tags=["Purchase"])
purchase_router.post('', response_model=ResponseContentDTO)(PurchaseController.create_purchase)
purchase_router.get('/{id}', response_model=PurchaseDTO)(PurchaseController.get_purchase)
purchase_router.delete('/{id}', response_model=ResponseContentDTO)(PurchaseController.delete_purchase)

bank_account_router = APIRouter(prefix="/bank_account", tags=["Bank account"])
bank_account_router.post('', response_model=ResponseContentDTO)(BankAccountController.create_bank_account)
bank_account_router.get('/{id}', response_model=BankAccountDTO)(BankAccountController.get_bank_account)
bank_account_router.get('', response_model=list[BankAccountDTO])(BankAccountController.get_all_bank_accounts)
bank_account_router.delete('/{id}', response_model=ResponseContentDTO)(BankAccountController.delete_bank_account)
bank_account_router.delete('', response_model=ResponseContentDTO)(BankAccountController.delete_all_bank_accounts)
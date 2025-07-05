import os
import sys
sys.path.append(os.getcwd())
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from DTO import CurrencyRateResponseDTO
from models import Currency, CurrencyRate
from database.base.database import Database
from database.seeders.base.base_seeder import BaseSeeder
from services.currencies_service import CurrenciesService

load_dotenv()

class CurrencyRatesUpdater(BaseSeeder):
    async def update(self) -> None:
        response = await CurrenciesService().get_rates()
        root = ET.fromstring(response.text)
        currency_rates = []

        for item in root.findall('item'):
            currency_rate = CurrencyRateResponseDTO(
                title=item.find('title').text, 
                rate=float(item.find('description').text)
            )

            currency_rates.append(currency_rate)

        currencies = await Currency().get_all()
        currency_titles = list(map(lambda currency: currency.currency, currencies))

        currency_rates = list(filter(
            lambda currency_rate: currency_rate.title in currency_titles, 
            currency_rates
        ))

        currency_rates = sorted(
            currency_rates, 
            key=lambda currency_rate: currency_titles.index(currency_rate.title)
        )

        currency_rates_models = []

        for currency_rate in currency_rates:
            currency_rates_models.append(CurrencyRate(
                currency_id=self.get_related(currencies, currency=currency_rate.title).id, 
                rate=currency_rate.rate
            ))

        await Database().seed([
            CurrencyRate(
                currency_id=self.get_related(currencies, currency='KZT').id, 
                rate=1
            ),
            *currency_rates_models
        ])
        
        print(f'INFO:     Successfully updated currency rates')
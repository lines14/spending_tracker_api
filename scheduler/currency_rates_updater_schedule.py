import os
import sys

sys.path.append(os.getcwd())
import xml.etree.ElementTree as ET

from dotenv import load_dotenv

from db.seeders.base.base_seeder import BaseSeeder
from dto import CurrencyRateResponseDTO
from models import Currency, CurrencyRate
from repositories.currencies_repository import CurrenciesRepository

load_dotenv()


class CurrencyRatesUpdaterSchedule(BaseSeeder):
    def __init__(self):
        super().__init__(CurrencyRate)

    async def update_currency_rates(self) -> None:
        currency_rates = []
        response = await CurrenciesRepository().get_rates()
        root = ET.fromstring(response.text)

        for item in root.findall("item"):
            currency_rate = CurrencyRateResponseDTO(
                title=item.find("title").text, rate=float(item.find("description").text)
            )

            currency_rates.append(currency_rate)

        currencies = await self.get_related_records(Currency)
        currency_titles = [currency.currency for currency in currencies]

        currency_rates = list(filter(lambda currency_rate: currency_rate.title in currency_titles, currency_rates))

        currency_rates = sorted(currency_rates, key=lambda currency_rate: currency_titles.index(currency_rate.title))

        currency_rates_models = []

        for currency_rate in currency_rates:
            currency_rates_models.append(
                CurrencyRate(
                    currency_id=self.get_related(currencies, currency=currency_rate.title).id, rate=currency_rate.rate
                )
            )

        data_list = [
            CurrencyRate(currency_id=self.get_related(currencies, currency="KZT").id, rate=1),
            *currency_rates_models,
        ]

        await self.seed(data_list)

        print("INFO:     [Scheduler] Successfully updated currency rates")

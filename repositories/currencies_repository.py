from datetime import UTC, datetime
from os import getenv

from dto import CurrencyRateRequestDTO
from repositories.base.http_client import HTTPClient


class CurrenciesRepository(HTTPClient):
    def __init__(self):
        super().__init__(base_url=getenv("CURRENCY_RATES_URL"))

    async def get_rates(self):
        params = CurrencyRateRequestDTO(fdate=datetime.now(UTC).strftime("%d.%m.%Y"))

        return await self.get("/rss/get_rates.cfm", params.model_dump())

from os import getenv
from datetime import datetime
from DTO import CurrencyRateRequestDTO
from services.base.HTTP_client import HTTPClient

class CurrenciesService(HTTPClient):
    def __init__(self):
        super().__init__(
            base_URL=getenv('CURRENCY_RATES_URL')
        )

    async def get_rates(self):
        params = CurrencyRateRequestDTO(
            fdate=datetime.now().strftime('%d.%m.%Y')
        )
        
        return await self.get('/rss/get_rates.cfm', vars(params))
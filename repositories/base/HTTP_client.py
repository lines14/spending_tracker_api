import httpx

class HTTPClient:
    def __init__(self, base_URL, timeout=None, headers=None):
        self.__client = httpx.AsyncClient(
            base_url=base_URL,
            headers=headers,
            timeout=timeout
        )

    async def get(self, endpoint, params=None):
        return await self.__client.get(url=endpoint, params=params)

    async def post(self, endpoint, data=None):
        return await self.__client.post(url=endpoint, data=data)

    async def put(self, endpoint, data=None):
        return await self.__client.put(url=endpoint, data=data)

    async def patch(self, endpoint, data=None):
        return await self.__client.patch(url=endpoint, data=data)

    async def delete(self, endpoint):
        return await self.__client.delete(url=endpoint)
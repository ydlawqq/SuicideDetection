import logging
import httpx


logger = logging.getLogger(__name__)


class Client:
    def __init__(self, base_url, timeout: float = 10.0):
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)


    async def predict(self, texts: list[str])-> list[float]:
        try:
            response = await self._client.post(
                "/predict",
                json={'texts': texts}
            )

            response.raise_for_status()

        except httpx.HTTPError as e:
            logger.warning('Модель не доступна: %s', e)
            raise httpx.HTTPError


        return response.json()['scores']

    async def aclose(self):
        await self._client.aclose()
        
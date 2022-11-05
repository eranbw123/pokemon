from httpx import AsyncClient, Response


async def async_client_fetch(url: str, client: AsyncClient) -> Response:
    return await client.get(url)

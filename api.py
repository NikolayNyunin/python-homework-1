import aiohttp


async def get_current_temperature(city: str, api_key: str) -> (int, float | str):
    """Получить текущую температуру в городе `city`."""

    api_url = 'https://api.openweathermap.org/data/2.5/weather'

    try:
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    return 0, (await response.json())['main']['temp']
                else:
                    return -1, await response.text()
    except aiohttp.ClientError as e:
        return -1, str(e)

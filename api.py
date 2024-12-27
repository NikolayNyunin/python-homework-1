import aiohttp
from dotenv import load_dotenv

import os

load_dotenv()


async def get_current_temperature(city: str, api_key: str = None) -> (int, float):
    """Получить текущую температуру в городе `city`."""

    api_url = 'https://api.openweathermap.org/data/2.5/weather'

    try:
        if api_key is None:
            api_key = os.getenv('API_KEY')
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                return 0, (await response.json())['main']['temp']
    except KeyError:
        return 1, 0.0
    except aiohttp.ClientError:
        return 2, 0.0

import pandas as pd

from concurrent.futures import ProcessPoolExecutor
from itertools import repeat

DATA_PATH = 'data/temperature_data.csv'


def is_anomaly(row: pd.Series) -> bool:
    """Проверка строки на аномальность."""

    return (row['temperature'] < row['rolling_mean'] - 2 * row['rolling_std']
            or row['temperature'] > row['rolling_mean'] + 2 * row['rolling_std'])


def calculate_stats(data: pd.DataFrame, city: str) -> dict:
    """Вычисление статистик."""

    result = {}
    for season in data['season'].unique():
        result[season] = {}
        result[season]['mean'] = data[(data['city'] == city) & (data['season'] == season)]['temperature'].mean()
        result[season]['std'] = data[(data['city'] == city) & (data['season'] == season)]['temperature'].std()
    return result


def analyze_data_mult() -> (pd.DataFrame, dict):
    """Анализ данных с мультипроцессностью."""

    # Загрузка данных
    data = pd.read_csv(DATA_PATH)

    # Скользящее среднее
    data['rolling_mean'] = data.groupby('city')['temperature'].transform(lambda x: x.rolling(window=30).mean())

    # Скользящее стандартное отклонение
    data['rolling_std'] = data.groupby('city')['temperature'].transform(lambda x: x.rolling(window=30).std())

    # Аномалии
    data['is_anomaly'] = data.apply(is_anomaly, axis=1)

    # Статистики
    with ProcessPoolExecutor() as executor:
        cities = data['city'].unique()
        results = executor.map(calculate_stats, repeat(data, len(cities)), cities)
        stats = {key: value for key, value in zip(cities, results)}

    return data, stats

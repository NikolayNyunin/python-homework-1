import pandas as pd

from datetime import date


def calculate_rolling_mean(data: pd.DataFrame) -> pd.Series:
    """Вычисление скользящего среднего для одного города."""

    return data['temperature'].rolling(window=30).mean()


def calculate_rolling_std(data: pd.DataFrame) -> pd.Series:
    """Вычисление скользящего стандартного отклонения для одного города."""

    return data['temperature'].rolling(window=30).std()


def calculate_stats(data: pd.DataFrame) -> dict:
    """Вычисление статистик для одного города."""

    stats = {}

    for season in data['season'].unique():
        temps = data[data['season'] == season]['temperature']
        stats[season] = {'mean': temps.mean(), 'std': temps.std()}

    return stats


def is_anomaly(row: pd.Series) -> bool:
    """Проверка строки на аномальность."""

    return (row['temperature'] < row['rolling_mean'] - 2 * row['rolling_std']
            or row['temperature'] > row['rolling_mean'] + 2 * row['rolling_std'])


def detect_anomalies(data: pd.DataFrame) -> pd.Series:
    """Поиск аномалий в температурных данных для одного города."""

    return data.apply(is_anomaly, axis=1)


def get_current_season() -> str:
    """Получение текущего времени года."""

    month_to_season = {12: 'winter', 1: 'winter', 2: 'winter',
                       3: 'spring', 4: 'spring', 5: 'spring',
                       6: 'summer', 7: 'summer', 8: 'summer',
                       9: 'autumn', 10: 'autumn', 11: 'autumn'}

    return month_to_season[date.today().month]

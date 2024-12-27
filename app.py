from api import get_current_temperature
from stats import calculate_rolling_average, calculate_stats, detect_anomalies, get_current_season

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import asyncio


async def main() -> None:
    """Точка входа Streamlit-приложения."""

    st.set_page_config(
        page_title='Анализ температуры',
        page_icon='🌡️',
        layout='wide'
    )

    # Задание пользовательских стилей
    style = """
    <style>
        div {text-align: center;}
    </style>
    """
    st.markdown(style, unsafe_allow_html=True)

    st.title('Домашнее задание №1 (Applied Python)')
    st.write('## Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API')
    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        data_file = st.file_uploader('Файл с историческими данными:', 'csv')
        if data_file is not None:
            data = pd.read_csv(data_file)
            cities = sorted(data['city'].unique())
            with col2:
                city = st.selectbox('Город для анализа:', cities, None)
        else:
            data = None
            with col2:
                city = st.selectbox('Город для анализа:', None, None)

    with col3:
        api_key = st.text_input('Ключ для OpenWeatherMap API:', None)

    analyze_button = st.button('Проанализировать температуру')
    st.divider()
    if analyze_button:
        await analyze_temperature(data, city, api_key)


async def analyze_temperature(data: pd.DataFrame, city: str, api_key: str) -> None:
    """Получение и анализ температуры в городе `city`."""

    if data is None:
        st.error('Файл с историческими данными не выбран')
        return
    elif city is None:
        st.error('Город для анализа не выбран')
        return
    elif api_key is None:
        st.error('Ключ для API не введён')
        return

    status_code, temperature = await get_current_temperature(city, api_key)
    if status_code != 0:
        st.error('Ошибка получения текущей температуры')
        return

    city_data = data[data['city'] == city]
    city_data['timestamp'] = pd.to_datetime(city_data['timestamp'])
    city_data['avg_temperature'] = calculate_rolling_average(city_data)
    city_stats = calculate_stats(city_data)
    city_data['is_anomaly'] = detect_anomalies(city_data, city_stats)

    st.write(f'## Текущая температура: ${temperature}°C$')
    current_season = get_current_season()
    mean, std = city_stats[current_season]['mean'], city_stats[current_season]['std']
    min_temp, max_temp = mean - 2 * std, mean + 2 * std
    if min_temp <= temperature <= max_temp:
        st.write(f'### :green-background[Температура в пределах нормального диапазона ({min_temp:.2f} ... {max_temp:.2f})]')
    else:
        st.write(f'### :red-background[Температура за пределами нормального диапазона ({min_temp:.2f} ... {max_temp:.2f})]')

    st.write('## Исторические данные:')

    st.write('### Статистики по сезонам:')
    city_stats_data = pd.DataFrame(city_stats)
    st.columns(3)[1].table(city_stats_data)

    st.write('### График истории температур:')
    not_anomalies = city_data[city_data['is_anomaly'] == False]
    anomalies = city_data[city_data['is_anomaly'] == True]
    fig, ax = plt.subplots(figsize=(12, 3))
    ax.scatter(not_anomalies['timestamp'], not_anomalies['temperature'], s=5, c='blue')
    ax.scatter(anomalies['timestamp'], anomalies['temperature'], s=5, c='red')
    ax.plot(city_data['timestamp'], city_data['avg_temperature'], c='lime', linewidth=2)
    st.pyplot(fig)
    st.write('(:blue[синий] - нормальные температуры, :red[красный] - аномалии, :green[зелёный] - скользящее среднее)')


if __name__ == '__main__':
    asyncio.run(main())

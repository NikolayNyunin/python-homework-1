from api import get_current_temperature

import streamlit as st
import pandas as pd

import asyncio


async def main() -> None:
    """Точка входа Streamlit-приложения."""

    st.set_page_config(
        layout='wide',
        page_title='Анализ температуры (ДЗ 1)',
        page_icon='🌡️'
    )

    st.title('Домашнее задание №1 (Applied Python)')
    st.write('## Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API')

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

    if st.button('Проанализировать температуру'):
        await analyse_temperature(data, city, api_key)


async def analyse_temperature(data: pd.DataFrame, city: str, api_key: str) -> None:
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

    st.write(f'### Текущая температура: ${temperature}°C$')


if __name__ == '__main__':
    asyncio.run(main())

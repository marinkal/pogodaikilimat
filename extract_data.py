from bs4 import BeautifulSoup as bsoup

import pandas as pd
import requests
import datetime
import calendar

URL = "https://pogodaiklimat.ru/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": URL,
    "Connection": "keep-alive",
}
YEARS = (i for i in range(2016, 2026))
print(YEARS)
ID = 28367
COLUMNS = ['Город', 'Дата', 'Минимум, °C', 'Средняя, °C', 'Максимум, °C', 'Отклонение от нормы', 'Осадки, мм']
FLOAT_COLUMNS =  ['Минимум, °C', 'Средняя, °C', 'Максимум, °C', 'Отклонение от нормы', 'Осадки, мм']

data = []
for year in YEARS:
    for m in range(1, 13):  # 12 месяцев в году
        url = f"{URL}monitor.php?id={ID}&month={m}&year={year}"
        response = requests.get(url=url, headers=HEADERS)
        if response.status_code == 200:
            content = response.content
            soup = bsoup(response.text, 'html.parser')
            rows = soup.select('.climate-table-wrap table tr')
            for index, row in enumerate(rows):
                if index < 2:
                    continue
                cells = ['Тюмень'] + [td.get_text(strip=True) for td in row.find_all('td')]
                if m == 2 and cells[1] == '29' and not calendar.isleap(year):
                    continue
                #print(cells[1], m, year)
                dt = datetime.date(year=year, month=m, day=int(cells[1]))
                print(dt)
                cells[1] = dt
                data.append(cells)
        else:
            print(response.status_code)
            
df = pd.DataFrame(data, columns=COLUMNS)
for column in FLOAT_COLUMNS:
    df[column] = pd.to_numeric(df[column], errors='coerce')

df.to_csv('climate_data.csv', index=False, encoding='utf-8-sig')
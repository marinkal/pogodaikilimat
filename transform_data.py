import pandas as pd


month_names = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентябрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}

season_map = {
    12: "Зима",
    1: "Зима",
    2: "Зима",
    3: "Весна",
    4: "Весна",
    5: "Весна",
    6: "Лето",
    7: "Лето",
    8: "Лето",
    9: "Осень",
    10: "Осень",
    11: "Осень",
}

df = pd.read_csv("climate_data.csv")
df["Амплитуда, °C"] = df["Максимум, °C"] - df["Минимум, °C"]
df["Дата"] = pd.to_datetime(df["Дата"])
df["Год"] = df["Дата"].dt.year
df["Месяц"] = df["Дата"].dt.month
df["Название месяца"] = df["Месяц"].map(month_names)
df["День года"] = df["Дата"].dt.day_of_year
df = df.round(1)
df.to_csv("daily_data.csv", index=False, encoding="utf-8-sig")

monthly = (
    df.groupby(["Год", "Месяц"])
    .agg(
        Сумма_осадков=("Осадки, мм", "sum"),
        Макс_температура=("Максимум, °C", "max"),
        Мин_температура=("Минимум, °C", "min"),
        Средняя_температура=("Средняя, °C", "mean"),
        Макс_амплитуда=("Амплитуда, °C", "max"),
        Средняя_амплитуда=("Амплитуда, °C", "mean"),
        Количество_дней=("Дата", "count"),  # полезно для контроля
    )
    .reset_index()
)
monthly["Название месяца"] = monthly["Месяц"].map(month_names)
monthly["Сезон"] = monthly["Месяц"].map(season_map)
monthly = monthly.round(1)

# Сохраняем
monthly.to_csv("monthly_summary.csv", index=False, encoding="utf-8-sig")

yearly = (
    df.groupby("Год").agg(
        Макс_температура=("Максимум, °C", "max"),
        Мин_температура=("Минимум, °C", "min"),
        Макс_амплитуда=("Амплитуда, °C", "max"),
        Сумма_осадков=("Осадки, мм", "sum"),
        Средняя_температура=("Средняя, °C", "mean"),
    ).reset_index()
)

for col, target, label in [
    ("Макс_температура", "Максимум, °C", "Дата_макс_температуры"),
    ("Мин_температура", "Минимум, °C", "Дата_мин_температуры"),
    ("Макс_амплитуда", "Амплитуда, °C", "Дата_макс_амплитуды"),
]:
    idx = df.groupby('Год')[target].idxmin() if 'Мин' in col else df.groupby('Год')[target].idxmax()
    dates = df.loc[idx, ["Год", "Дата"]].set_index("Год")["Дата"]
    yearly[label] = yearly["Год"].map(dates)

yearly = yearly.round(1)
yearly.to_csv("yearly_summary.csv", index=False, encoding="utf-8-sig")

print(yearly)
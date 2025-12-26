import pandas as pd
import os

print("Current working directory:", os.getcwd())

df = pd.read_csv(
    r"C:\Users\yuvra\OneDrive\Desktop\Weather-Forecasting-Project\data\weather_kaggle.csv"
)

df = df.rename(columns={
    "meantemp": "temp",
    "wind_speed": "wind"
})

df["temp_next_day"] = df["temp"].shift(-1)
df.dropna(inplace=True)

output_path = r"C:\Users\yuvra\OneDrive\Desktop\Weather-Forecasting-Project\data\cleaned_weather.csv"
df.to_csv(output_path, index=False)

print("Cleaned data saved at:", output_path)

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle

df = pd.read_csv(
    r"C:\Users\yuvra\OneDrive\Desktop\Weather-Forecasting-Project\data\cleaned_weather.csv"
)

X = df[["temp", "humidity", "wind"]]
y = df["temp_next_day"]

model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X, y)

with open(
    r"C:\Users\yuvra\OneDrive\Desktop\Weather-Forecasting-Project\model\weather_model.pkl",
    "wb"
) as f:
    pickle.dump(model, f)

print("Model trained and saved successfully")

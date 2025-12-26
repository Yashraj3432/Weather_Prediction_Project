from pydantic import BaseModel

class Register(BaseModel):
    username: str
    password: str

class Login(BaseModel):
    username: str
    password: str

class WeatherInput(BaseModel):
    temp: float
    humidity: float
    wind: float

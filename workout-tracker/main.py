import requests
import os
from dotenv import load_dotenv

load_dotenv()

gender = os.getenv("GENDER")
weight = os.getenv("WEIGHT_KG")
height= os.getenv("HEIGHT_CM")
age = os.getenv("AGE")


app_id = os.getenv("APP_ID")
api_key = os.getenv("API_KEY")


exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": app_id,
    "x-app-key": api_key,
}

parameters = {
    "query": exercise_text,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)
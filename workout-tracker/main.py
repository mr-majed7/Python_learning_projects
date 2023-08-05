import requests
import os
from dotenv import load_dotenv
import datetime

date = datetime.date.today()
formatted_date = date.strftime('%d/%m/%Y')

current_time = datetime.datetime.now().time()
formatted_time = current_time.strftime('%H:%M:%S')

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

sheet_url = os.getenv("SHEET_URL")
bearer_headers = {
"Authorization": os.getenv("BEARER_TOKEN")
}

for exercise in result["exercises"]:
    data = {
        "workout":{
            "date": formatted_date,
            "time": formatted_time,
            "exercise":exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories":exercise["nf_calories"]
        }
    }
    sheet_response = requests.post(sheet_url, json=data,headers=bearer_headers)
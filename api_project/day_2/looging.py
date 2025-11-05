import requests
import logging

# הגדרת לוג בסיסי
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# מפתח אישי מהאתר (לא אמיתי כאן)
API_KEY = "YOUR_API_KEY"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city: str):
    params = {
        "q": city,             # שם העיר
        "appid": API_KEY,      # מפתח הגישה
        "units": "metric"      # יחידות מידה (צלזיוס)
    }

    try:
        logging.info(f"Fetching weather for {city}")
        response = requests.get(BASE_URL, params=params, timeout=(2, 8))
        response.raise_for_status()  # אם קוד שגיאה – נזרוק חריגה
        data = response.json()

        # שליפה מתוך ה־JSON
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        logging.info(f"{city}: {temp}°C, {desc}")
        return {"city": city, "temp": temp, "desc": desc}

    except requests.exceptions.Timeout:
        logging.error("⏱️ Timeout – השרת לא הגיב בזמן")
    except requests.exceptions.ConnectionError:
        logging.error("🔌 ConnectionError – בעיית רשת")
    except requests.exceptions.HTTPError as e:
        logging.error(f"⚠️ HTTPError: {e.response.status_code}")
    except Exception as e:
        logging.critical(f"❌ Unexpected error: {e}")

# דוגמה להרצה
if __name__ == "__main__":
    result = get_weather("Tel Aviv")
    if result:
        print(result)

import requests
import csv
import os
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("OPENWEATHER_API_KEY")



# Function to get weather data
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["description"].capitalize()
            country = data["sys"]["country"]
            wind_speed = data["wind"]["speed"]

            result = {
                "City": city,
                "Country": country,
                "Temperature (°C)": temp,
                "Humidity (%)": humidity,
                "Condition": condition,
                "Wind Speed (m/s)": wind_speed
            }

            return result
        else:
            print(f"❌ City '{city}' not found.")
            return None
    except Exception as e:
        print("❌ Error occurred:", e)
        return None

# Function to save to CSV
def save_to_csv(data, filename="weather_output.csv"):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Main function
def main():
    print("🌦️ Welcome to the Weather CLI App 🌦️\n")

    while True:
        city = input("🔍 Enter city name: ").strip()
        weather_data = get_weather(city)

        if weather_data:
            print("\n📍 Weather Details:")
            for key, value in weather_data.items():
                print(f"{key}: {value}")

            save = input("\n💾 Do you want to save this result to CSV? (yes/no): ").strip().lower()
            if save == 'yes':
                save_to_csv(weather_data)
                print("✅ Saved to weather_output.csv")

        another = input("\n🔁 Do you want to check another city? (yes/no): ").strip().lower()
        if another != 'yes':
            print("\n👋 Exiting... Stay safe and check the weather daily!")
            break

# Run app
if __name__ == "__main__":
    main()

from flask import Flask, jsonify, request, render_template
import requests
import psycopg2

app = Flask(__name__)

API_KEY = "ac9518e6565290318151181a101b0fb3"

# Database connection
try:
    conn = psycopg2.connect(
        dbname="weather_db",
        user="postgres",
        password="newpassword123",
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city TEXT,
    temperature FLOAT,
    humidity FLOAT,
    pressure FLOAT,
    wind FLOAT,
    condition TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
    conn.commit()

    print("✅ Database connected successfully")

except Exception as e:
    print("❌ Database error:", e)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/weather")
def get_weather():

    try:
        city = request.args.get("city", "London")

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

        response = requests.get(url).json()

        if response.get("cod") != 200:
            return jsonify({"error": "City not found"})

        temp = response["main"]["temp"]
        humidity = response["main"]["humidity"]
        pressure = response["main"]["pressure"]
        wind = response["wind"]["speed"]
        condition = response["weather"][0]["main"]

        # Save to DB safely
        try:
            cursor.execute("""
                INSERT INTO weather_data 
                (city, temperature, humidity, pressure, wind, condition)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (city, temp, humidity, pressure, wind, condition))

            conn.commit()

        except Exception as db_error:
            print("❌ DB Insert Error:", db_error)
            conn.rollback()

        return jsonify({
            "city": city,
            "temp": temp,
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "condition": condition,
           
        })

    except Exception as e:
        print("❌ Weather API error:", e)
        return jsonify({"error": "Server error"})


if __name__ == "__main__":
    app.run(debug=True)

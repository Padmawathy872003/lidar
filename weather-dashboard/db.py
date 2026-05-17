import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="weather_db",
    user="postgres",
    password="newpassword123"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(50),
    temperature FLOAT,
    description TEXT
)
""")

conn.commit()
print("Database connected and table created!")
conn.close()

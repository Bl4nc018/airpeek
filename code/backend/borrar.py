import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Cambia o añade tablas si lo necesitas
tables = [
    "airpeek_api_flights",
    "airpeekbackendapp_flights",
]

for table in tables:
    cursor.execute(f"DELETE FROM {table};")
    print(f"Los vuelos de la tabla {table} se han vaciado correctamente.")

conn.commit()
conn.close()

print("Las tablas de los vuelos se han vaciado correctamente")

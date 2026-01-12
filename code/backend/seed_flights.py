#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
seed_flights.py
Inserta vuelos de prueba en db.sqlite3 (tablas tipo: airpeek_api_flights / airpeekbackendapp_flights)

Cómo usar este script:
    python seed_flights.py
    python seed_flights.py --n 50
    python seed_flights.py --reset
    python seed_flights.py --db ./db.sqlite3 --n 200 --reset
"""

import argparse
import os
import random
import sqlite3
import string
from datetime import datetime, timedelta
from decimal import Decimal

DEFAULT_TABLE_CANDIDATES = [
    "airpeek_api_flights",
    "airpeekbackendapp_flights",
]

# Orígenes/destinos (valen hasta varchar(20)). Puedes editar libremente.
AIRPORTS = [
    "MAD", "BCN", "SVQ", "VLC", "BIO", "AGP", "PMI", "LPA",
    "LIS", "OPO", "CDG", "ORY", "LHR", "LGW", "AMS", "FRA",
    "MUC", "ZRH", "MXP", "FCO", "VIE", "PRG", "WAW", "CPH",
    "ARN", "OSL", "DUB", "BRU", "ATH", "IST",
]

BUY_URLS = [
    "https://example.com/buy",
    "https://example.com/checkout",
    "https://example.com/tickets",
]


def table_exists(cur: sqlite3.Cursor, table_name: str) -> bool:
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        (table_name,),
    )
    return cur.fetchone() is not None


def get_existing_flight_codes(cur: sqlite3.Cursor, table: str) -> set[str]:
    cur.execute(f"SELECT flight FROM {table};")
    return {row[0] for row in cur.fetchall()}


def make_flight_code(existing: set[str]) -> str:
    # PK es varchar(10)
    # Formato: AP + 4 dígitos + 2 letras (8 chars) o variante similar.
    while True:
        code = "AP" + "".join(random.choices(string.digits, k=4)) + "".join(
            random.choices(string.ascii_uppercase, k=2)
        )
        code = code[:10]
        if code not in existing:
            existing.add(code)
            return code


def random_route() -> tuple[str, str]:
    origin = random.choice(AIRPORTS)
    dest = random.choice([a for a in AIRPORTS if a != origin])
    return origin, dest


def dt_to_db_string(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S") # Django guarda datetime como "YYYY-MM-DD HH:MM:SS"


def random_price() -> str:
    value = Decimal(random.randint(25, 450)) + (Decimal(random.randint(0, 99)) / 100) # Columna 'price' es decimal. Guardamos como texto con 2 decimales.
    return f"{value:.2f}"


def seed_table(conn: sqlite3.Connection, table: str, n: int, reset: bool) -> int:
    cur = conn.cursor()

    if reset:
        cur.execute(f"DELETE FROM {table};")
        conn.commit()

    existing_codes = get_existing_flight_codes(cur, table)

    rows = []
    now = datetime.now()

    for _ in range(n):
        flight = make_flight_code(existing_codes)
        origin, destination = random_route()

        dep = now + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(0, 23),
            minutes=random.choice([0, 15, 30, 45]),
        )
        
        arr = dep + timedelta(hours=random.randint(1, 6), minutes=random.choice([0, 15, 30, 45]))

        price = random_price()
        buy_url = random.choice(BUY_URLS) + f"?flight={flight}"

        rows.append(
            (
                flight,
                origin,
                destination,
                dt_to_db_string(dep),
                dt_to_db_string(arr),
                price,
                buy_url,
            )
        )

    cur.executemany(
        f"""
        INSERT INTO {table} (flight, origin, destination, departure_date, arrival_date, price, buyUrl)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """,
        rows,
    )
    conn.commit()
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description="Inserta vuelos de prueba en db.sqlite3")
    parser.add_argument("--db", default="db.sqlite3", help="Ruta a db.sqlite3 (por defecto: ./db.sqlite3)")
    parser.add_argument("--n", type=int, default=25, help="Número de vuelos a insertar por tabla (por defecto: 25)")
    parser.add_argument("--reset", action="store_true", help="Borra los vuelos existentes antes de insertar")
    parser.add_argument(
        "--tables",
        nargs="*",
        default=None,
        help="Lista de tablas a poblar (si no se indica, intenta con las conocidas)",
    )
    args = parser.parse_args()

    db_path = args.db
    if not os.path.exists(db_path):
        raise SystemExit(f"No existe la base de datos: {db_path}")

    tables_to_try = args.tables if args.tables else DEFAULT_TABLE_CANDIDATES

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        existing = [t for t in tables_to_try if table_exists(cur, t)]

        if not existing:
            raise SystemExit(
                "No encontré ninguna tabla de vuelos. Probé: "
                + ", ".join(tables_to_try)
                + "\nComprueba el nombre de la tabla o pasa --tables <nombre_tabla>."
            )

        total = 0
        for t in existing:
            inserted = seed_table(conn, t, args.n, args.reset)
            print(f"Tabla {t}: insertados {inserted} vuelos{' (reset previo)' if args.reset else ''}")
            total += inserted

        print(f"\nTotal insertado: {total} vuelos en {len(existing)} tabla(s).")
    finally:
        conn.close()


if __name__ == "__main__":
    random.seed()  # semilla aleatoria
    main()

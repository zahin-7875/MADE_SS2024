import requests
import zipfile
import os
import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

url = "https://www.mowesta.com/data/measure/mowesta-dataset-20221107.zip"
zip_path = "mowesta-dataset.zip"

logging.info(f"Downloading data from {url}")
response = requests.get(url)
with open(zip_path, 'wb') as file:
    file.write(response.content)

logging.info("Extracting zip file")
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall("mowesta-dataset")

csv_path = "mowesta-dataset/data.csv"
logging.info(f"Reading CSV file from {csv_path}")

df = pd.read_csv(csv_path, delimiter=';', quotechar='"', on_bad_lines='skip')

required_columns = ["Geraet", "Hersteller", "Model", "Monat", "Temperatur in °C (DWD)", "Batterietemperatur in °C"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    logging.error(f"Missing columns in the CSV file: {missing_columns}")
else:
    columns_to_keep = {
        "Geraet": "id",
        "Hersteller": "producer",
        "Model": "model",
        "Monat": "month",
        "Temperatur in °C (DWD)": "temperature",
        "Batterietemperatur in °C": "battery_temperature"
    }
    df = df[list(columns_to_keep.keys())].rename(columns=columns_to_keep)

    df['temperature'] = df['temperature'].astype(str).str.replace(',', '.').str.strip()
    df['battery_temperature'] = df['battery_temperature'].astype(str).str.replace(',', '.').str.strip()

    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['battery_temperature'] = pd.to_numeric(df['battery_temperature'], errors='coerce')

    df = df.dropna(subset=['temperature', 'battery_temperature'])

    df['temperature'] = df['temperature'].apply(lambda x: (x * 9/5) + 32 if pd.notnull(x) else x)
    df['battery_temperature'] = df['battery_temperature'].apply(lambda x: (x * 9/5) + 32 if pd.notnull(x) else x)

    df = df[df['id'].apply(lambda x: str(x).isdigit())]  # Ensure 'id' is numeric
    df['id'] = df['id'].astype(int)
    df = df[df['id'] > 0]

    if not df.empty:
        sqlite_file = 'temperatures.sqlite'
        conn = sqlite3.connect(sqlite_file)
        df.to_sql('temperatures', conn, if_exists='replace', index=False)
        conn.close()

os.remove(zip_path)
if os.path.exists(csv_path):
    os.remove(csv_path)
if os.path.exists("mowesta-dataset"):
    for filename in os.listdir("mowesta-dataset"):
        os.remove(os.path.join("mowesta-dataset", filename))
    os.rmdir("mowesta-dataset")

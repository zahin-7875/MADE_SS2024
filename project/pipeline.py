import os
import pandas as pd
import sqlite3
from kaggle.api.kaggle_api_extended import KaggleApi
import zipfile
import io

def initialize_kaggle_api():
    api = KaggleApi()
    api.authenticate()
    return api

def create_data_directory(path):
    os.makedirs(path, exist_ok=True)

def download_kaggle_dataset(api, dataset, filename, data_dir):
    api.dataset_download_file(dataset, filename, path=data_dir, force=True)
    downloaded_file_path = os.path.join(data_dir, filename)
    if os.path.exists(downloaded_file_path):
        return downloaded_file_path
    else:
        zip_file_path = f"{downloaded_file_path}.zip"
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        os.remove(zip_file_path)
        return downloaded_file_path

def load_csv(filepath):
    try:
        return pd.read_csv(filepath)
    except pd.errors.ParserError:
        with open(filepath, 'r', errors='replace') as file:
            content = file.read()
        return pd.read_csv(io.StringIO(content))

def filter_data(df, column, start_year, end_year):
    return df[(df[column] >= start_year) & (df[column] <= end_year)]

def store_data_in_sqlite(df, table_name, conn):
    df.to_sql(table_name, conn, if_exists="replace", index=False)

def main():
    datasets = {
        "greenhouse_gas": "unitednations/international-greenhouse-gas-emissions",
        "sea_ice": "nsidcorg/daily-sea-ice-extent-data"
    }

    data_dir = "D:\Summer 2024\Methods of Advanced Data Engineering (MADE)\Exercise_main\MADE_SS2024\data"
    sqlite_db_path = os.path.join(data_dir, "climate_data.db")

    create_data_directory(data_dir)
    
    api = initialize_kaggle_api()

    greenhouse_gas_path = download_kaggle_dataset(api, datasets["greenhouse_gas"], "greenhouse_gas_inventory_data_data.csv", data_dir)
    sea_ice_path = download_kaggle_dataset(api, datasets["sea_ice"], "seaice.csv", data_dir)

    ghg_df = load_csv(greenhouse_gas_path)
    sea_ice_df = load_csv(sea_ice_path)

    ghg_df = filter_data(ghg_df, 'year', 1990, 2014)
    sea_ice_df = filter_data(sea_ice_df, 'Year', 1990, 2014)

    ghg_df.dropna(inplace=True)
    sea_ice_df.dropna(inplace=True)

    conn = sqlite3.connect(sqlite_db_path)

    store_data_in_sqlite(ghg_df, "greenhouse_gas", conn)
    store_data_in_sqlite(sea_ice_df, "sea_ice", conn)

    conn.close()

if __name__ == "__main__":
    main()

print("Data pipeline executed successfully.")
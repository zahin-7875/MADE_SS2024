import pandas as pd
import sqlite3

# URL of the CSV file
csv_url = "https://www-genesis.destatis.de/genesis/downloads/00/tables/46131-0014_00.csv"

# Read the CSV file, skipping metadata rows and the footer, with semicolon as delimiter
df = pd.read_csv(csv_url, skiprows=8, skipfooter=5, engine='python', encoding='latin1', on_bad_lines='skip', delimiter=';')

# Clean the column names by stripping any extra whitespace
df.columns = df.columns.str.strip()

columns_to_select = ['2024', 'Januar', 'NST7-011', 'Getreide', 'Schleswig-Holstein', '278', '278.1']
df = df[columns_to_select]

# Rename the columns
new_column_names = ['year', 'month', 'goods_id', 'goods_name', 'goods_source', 'abroad', 'total']
df.columns = new_column_names

def clean_data(df):
    # Ensure 'year' and quantity columns are positive integers
    df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')
    df['abroad'] = pd.to_numeric(df['abroad'], errors='coerce').astype('Int64')
    df['total'] = pd.to_numeric(df['total'], errors='coerce').astype('Int64')

    # Ensure 'month' is a German month, capitalized
    german_months = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    df['month'] = df['month'].apply(lambda x: x if x in german_months else None)

    # Ensure 'goods_id' starts with NST7-
    df['goods_id'] = df['goods_id'].apply(lambda x: x if pd.notnull(x) and x.startswith('NST7-') else None)

    # Drop rows with missing or invalid values
    df.dropna(inplace=True)

    return df

df = clean_data(df)

conn = sqlite3.connect("goodsTransportedByTrain.sqlite")
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS goods (
    year INTEGER,
    month TEXT,
    goods_id TEXT,
    goods_name TEXT,
    goods_source TEXT,
    abroad INTEGER,
    total INTEGER
)
''')

# Insert the data into the SQLite database
df.to_sql('goods', conn, if_exists='replace', index=False, dtype={
    'year': 'BIGINT',
    'month': 'TEXT',
    'goods_id': 'TEXT',
    'goods_name': 'TEXT',
    'goods_source': 'TEXT',
    'abroad': 'BIGINT',
    'total': 'BIGINT'
})

conn.commit()
conn.close()

print("Data pipeline executed successfully.")
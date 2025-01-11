import pandas as pd
import sqlite3
from pathlib import Path

db_file = Path(__file__).parent.parent/'data/curated_factory.db'

def load_data(table_name):
    """
    Connects to the SQLite database and loads the data from the specified table.
    """
    try:
        conn = sqlite3.connect(db_file)
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql(query, conn)
        conn.close()
        return data
    except sqlite3.OperationalError as e:
        return pd.DataFrame({"Message": [f"Error: {e}. Please ensure the table '{table_name}' exists in the database."]})


def getFactoryComplexDataProfit(): 
    DATA_FILENAME = Path(__file__).parent.parent/'data/large-data/Complex_Expanded_Factory_Data.csv'
    raw_df =  pd.read_csv(DATA_FILENAME)

    from os import replace

    col_rename_lst = {}
    for series_name, series in raw_df.items():
        col_rename_lst[series_name] = series_name.replace(' ','_').replace('%','pcnt').replace('(','').replace(')','').replace('$','dolrs').lower()
    raw_df = raw_df.rename(columns=col_rename_lst)

    return raw_df


def create_sqlite_db_from_dataframe(df, db_path, table_name, if_exists='fail', index=False):
    """
    Creates a SQLite database and table from a Pandas DataFrame.

    Args:
        df (pd.DataFrame): The Pandas DataFrame to be stored.
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to create.
        if_exists (str, optional):  What to do if the table already exists.
            - 'fail': Raise a ValueError if the table already exists.
            - 'replace': Drop the table before inserting new values.
            - 'append': Append new values to the existing table.
            Defaults to 'fail'.
        index (bool, optional): Write DataFrame index as a column. Defaults to False.
    """
    
    try:
      Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    except:
      print("Error creating parent folder for db")
    

    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(table_name, conn, if_exists=if_exists, index=index)
        conn.close()
        print(f"DataFrame successfully written to table '{table_name}' in '{db_path}'.")
    except ValueError as e:
        print(f"Error writing DataFrame to SQLite: {e}")
    except sqlite3.Error as e:
      print(f"Sqlite Error: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def avg_defect_rate(filtered_factory_df):
    filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    filtered_factory_df['Year'] = pd.DatetimeIndex(filtered_factory_df['date']).year
    filtered_factory_df['MonthYear'] = filtered_factory_df['time'].apply("{:%Y-%m}".format)
    monthly_avg_df = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory'], filtered_factory_df['Year']])['defect_rate_pcnt'].mean().reset_index()
    return monthly_avg_df 

def production_vol(filtered_factory_df):
    filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    filtered_factory_df['Year'] = pd.DatetimeIndex(filtered_factory_df['date']).year
    filtered_factory_df['MonthYear'] = filtered_factory_df['time'].apply("{:%Y-%m}".format)
    avg_month_prod= filtered_factory_df.groupby([filtered_factory_df['MonthYear'],filtered_factory_df['factory'], filtered_factory_df['Year']])['production_volume_units'].mean().reset_index()
    return avg_month_prod

def energy_consumption_kwh(filtered_factory_df):
    filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    filtered_factory_df['Year'] = pd.DatetimeIndex(filtered_factory_df['date']).year
    filtered_factory_df['MonthYear'] = filtered_factory_df['time'].apply("{:%Y-%m}".format)
    avg_month_energy = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory'], filtered_factory_df['Year']])['energy_consumption_kwh'].mean().reset_index()
    return avg_month_energy

def downtime_factory(filtered_factory_df):
    filtered_factory_df['time'] = pd.to_datetime(filtered_factory_df['date'])
    filtered_factory_df['Year'] = pd.DatetimeIndex(filtered_factory_df['date']).year
    filtered_factory_df['MonthYear'] = filtered_factory_df['time'].apply("{:%Y-%m}".format)
    avg_month_dntime = filtered_factory_df.groupby([filtered_factory_df['MonthYear'], filtered_factory_df['factory'], filtered_factory_df['Year']])['machine_downtime_hours'].mean().reset_index()
    return avg_month_dntime



if __name__ == '__main__':
    filtered_factory_df = getFactoryComplexDataProfit()
    monthly_avg_df = avg_defect_rate(filtered_factory_df)
    create_sqlite_db_from_dataframe(monthly_avg_df, db_file, 'avg_defect_rate_table', if_exists='replace', index=True)

    avg_month_prod = production_vol(filtered_factory_df)
    create_sqlite_db_from_dataframe(avg_month_prod,db_file, 'production_volume_units', if_exists='replace', index=True)
    
    avg_month_energy = energy_consumption_kwh(filtered_factory_df)
    create_sqlite_db_from_dataframe(avg_month_energy,db_file, 'energy_consumption_kwh', if_exists='replace', index=True)

    avg_month_dntime = downtime_factory(filtered_factory_df)
    create_sqlite_db_from_dataframe(avg_month_dntime,db_file, 'machine_downtime_hours', if_exists='replace', index=True)



def get_defect_rate():
    load_data('avg_defect_rate_table')
    return load_data

def get_product_vol():
    load_data('production_volume_units')
    return load_data

def get_energy_consume():
    load_data('energy_consumption_kwh')
    return load_data

def get_downtime():
    load_data('machine_downtime_hours')
    return load_data






    

   
    

    
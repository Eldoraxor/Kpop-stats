import pandas as pd
import mysql.connector
import configparser
from sqlalchemy import create_engine

config = configparser.ConfigParser()
config.read('config.ini')
connector_dir = {"host" : "localhost",
                 "port" : 3306,
                 "user" : "root",
                 "password" : "SQLRom3821!",
                 "database" : "Kpop"}

def register_data(dataf: pd.DataFrame, table_name: str):
    mydb = mysql.connector.connect(**connector_dir)
    mycursor = mydb.cursor()

    engine = create_engine(f"mysql+mysqlconnector://{connector_dir['user']}:{connector_dir['password']}@{connector_dir['host']}:{connector_dir['port']}/{connector_dir['database']}")
    dataf.to_sql(table_name, con=engine, if_exists='replace', index=True, index_label= f"{table_name}_id")

    mydb.commit()
    mydb.close()

def get_sql_data(table_name: str) -> pd.DataFrame:
    mydb = mysql.connector.connect(**connector_dir)
    mycursor = mydb.cursor()

    engine = create_engine(f"mysql+mysqlconnector://{connector_dir['user']}:{connector_dir['password']}@{connector_dir['host']}:{connector_dir['port']}/{connector_dir['database']}")
    my_df = pd.read_sql_table(table_name, engine)

    mydb.commit()
    mydb.close()

    return my_df
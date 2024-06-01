import pyodbc

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=laptop-ttip97em\\sqlexpress;DATABASE=platt_reilly;Trusted_Connection=yes;')
    return conn
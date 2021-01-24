import numpy as np
import pandas as pd
import pyodbc 
import sqlalchemy
import urllib
import socket
import tools


def get_conn_string(srv: str, db_name: str) -> str:
    return f"Driver={{SQL Server}};Server={srv};Database={db_name};Trusted_Connection=yes;Timeout=600"


def get_connection(srv:str, db_name:str):
    """
    Generates the connection string using the specified server and database name
    """

    connection_string = get_conn_string(srv, db_name)
    return pyodbc.connect(connection_string)



def get_recordset(conn: object, query: str) -> pd.DataFrame:
    """Returns a list of databases given a specified connection"""
    
    cursor = conn.cursor()
    result = pd.read_sql_query(query, conn)
    return result


def exec_non_query(conn: object, cmd: str) -> int:
    """executes a command on the database"""

    result = 0
    try:
        cursor = conn.cursor()
        cursor.execute(cmd)
        conn.commit()
        result = 1
    except Exception as ex:
        print(ex)
        conn.rollback()
        result = 0
    return result

def get_value(conn: object, query: str) -> str:
    """
    return a single value for a specified query
    """
    result = pd.DataFrame()
    try:
        cursor = conn.cursor()
        result = pd.read_sql_query(query, conn)
    except Exception as ex:
        result = const.ERROR_CODE

    if len(result) > 0:
        return result['result'][0]
    else:
        return None


def get_db_value(value: str, type: int):
    result = ''
    if type == 1:
        result = f"'{value}'"
    elif type == 2:
        result = 'Null' if value in ('None','') else value
    elif type == 3:
        result = 'Null' if value in ('None','') else value.replace(',','.')
    return result
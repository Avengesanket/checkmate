import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def insert_cheque_data(data):
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cheques (
        cheque_no VARCHAR,
        date DATE,
        account_no VARCHAR,
        bank_name VARCHAR,
        payee_name VARCHAR,
        amount NUMERIC
    );
    ''')

    cursor.execute('''
    INSERT INTO cheques (cheque_no, date, account_no, bank_name, payee_name, amount)
    VALUES (%s, %s, %s, %s, %s, %s);
    ''', (
        data['cheque_no'],
        data['date'],
        data['account_no'],
        data['bank_name'],
        data['payee_name'],
        data['amount']
    ))

    connection.commit()
    cursor.close()
    connection.close()

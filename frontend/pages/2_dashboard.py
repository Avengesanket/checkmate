import pandas as pd
from database import insert_cheque_data
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_cheque_data():
    connection = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM cheques")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows

st.title("Dashboard")
data = fetch_cheque_data()
columns = ["Cheque No.", "Date", "Account No.", "Bank Name", "Payee Name", "Amount"]
df = pd.DataFrame(data, columns=columns)
st.write(df)

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="cheque_data.csv",
    mime="text/csv"
)
from unicodedata import category
import pyodbc

def connection():
    s = 'DESKTOP-O4OB08D\MAYCHU' 
    d = 'db_app' 
    u = 'sa'
    p = '123456'
    db_app = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    
    conn = pyodbc.connect(db_app)
    return conn

def login(query):
    data = []
    conn = connection()
    cursor = conn.cursor()
    data = cursor.execute(query).fetchall()
    conn.close()

    return data

def get_category(query):
    categories = []
    conn = connection()
    cursor = conn.cursor()
    categories = cursor.execute(query).fetchall()
    conn.close()

    return categories

def get_user(query):
    user = []
    conn = connection()
    cursor = conn.cursor()
    user = cursor.execute(query).fetchall()
    conn.close()

    return user

if __name__ == '__main__':
    query = 'SELECT * FROM dbo.user_app'
    op = login(query)
    print(op)

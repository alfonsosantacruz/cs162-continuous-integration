import requests
import psycopg2
from sqlalchemy import create_engine

# Format: "postgres+psycopg2://<USERNAME>:<PASSWORD>@<IP_ADDRESS>:<PORT>/<DATABASE_NAME>"
DATABASE_URI = 'postgres+psycopg2://cs162_user:cs162_password@192.168.99.100:5432/cs162'
engine = create_engine(DATABASE_URI, echo=True)

connection = engine.connect()


def test_response():
    response = requests.post('http://192.168.99.100:5000/add',data={'expression':'5+5'})
    assert response.status_code == 200

def test_db():
    res = connection.execute("SELECT * FROM Expression WHERE text='5+5' LIMIT 1").fetchall()
    # print(res)
    assert res[0][2] == 10

def test_error():
    response = requests.post('http://192.168.99.100:5000/add', data={'expression':'2/0'})
    assert response.status_code == 500

def test_exp():
    res = connection.execute("SELECT * FROM Expression ORDER BY id DESC LIMIT 1").fetchall()
    # print(res)
    assert res[0][1] == '5+5'

if __name__=="__main__":
    print("Running Tests")
    test_response()
    test_db()
    test_error()
    test_exp()
    print("All passed")

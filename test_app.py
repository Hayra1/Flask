import pytest 
from app import app
import json 

file = open("books.json")
data = json.load(file)

file_2 = open("all_reviews.json")
data_2 = json.load(file_2)

file_3 = open("books_id_1.json")
data_3 = json.load(file_3)


@pytest.fixture()
def client():
    return app.test_client()



def test_request_example(client):
    response = client.get("/")
    json_respons = response.text
    assert json_respons == "Hello!"
    


def test_endpoint_all_books(client):
    respons = client.get("/all_books")
    resons_js = respons.json
    assert resons_js == data


def test_endpoint_all_reviews(client):
    respons = client.get("/all_reviews")
    respons_json = respons.json
    assert respons_json == data_2

def test_endpoint_books_id (client):
    respons = client.get("/books?id=1")
    respons_json = respons.json
    assert respons_json == data_3

def test_endpoint_author_sergey(client):
    res = client.get("/author?=Sergey Hayrapetyan")
    res_text = res.text
    assert res_text == """None may refer to:Zero, the mathematical concept of the quantity "none"
Empty set, the mathematical concept of the collection of things represented by "none"
none, an indefinite pronoun in the English language"""""
    
    
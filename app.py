from flask import Flask, request, jsonify

import requests

import sqlite3

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello!"

DATABASE = '/Users/sergey/Desktop/Databas/Bocker.db'


#Söker efter alla böcker i databasen 
@app.route("/all_books")
def get_books():
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM bocker")
        all_books = cursor.fetchall()
    return jsonify({"books": all_books})


#Söker efter enskilda böckers id,titel och författare
#har även gjort att den söker efter författare och titlar som liknar varandra, därför jag har % runt de
@app.route("/books")
def search_for_book():
    titel = request.args.get("titel", None)
    book_id = request.args.get("id", None)
    forfattare = request.args.get("forfattare", None)
    query = "SELECT * FROM bocker WHERE 1 "
    

    if titel:
        query += f"AND title LIKE '%{titel}%'"

    if book_id:
        query += f"AND id LIKE '{book_id}'"

    if forfattare:
        query += f"AND forfattare LIKE '%{forfattare}%'"

    connection = sqlite3.connect("Bocker.db")
    cursor = connection.cursor()
    

    res = cursor.execute(query).fetchall()
   
    return res



#lägger till böcker i databasen, man måste ange id,titel,författare,sammafattning och genre 
#för att den ska lägga till boken 
@app.route("/books",methods = ["POST"])
def add_new_books():
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        new_books = request.json
        for books in new_books:
            cursor.execute("INSERT INTO bocker (id,titel,forfattare,sammanfattning,genre) VALUES (?,?,?,?,?)",
                       (books["id"], books["titel"], books["forfattare"], books["sammanfattning"],books["genre"]))
    return "Books added successfully"



#Uppdaterar titel på en bok som redan finns i databasen 
@app.route("/update_books/<int:book_id>", methods = ["PUT"])
def uppdate_books (book_id):
    new_title = request.json.get("titel")
    if not new_title:
        return jsonify({"error": "Missing 'new_title' in the request body"})
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE bocker SET titel = ? WHERE id = ?", (new_title,book_id))
    
    return "Updated successfully"


#Tar bort en bok från databasen 
@app.route("/delete_book/<int:book_id>", methods =["DELETE"])
def delete_books(book_id):
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM bocker WHERE id = ?",(book_id,))

    return "Book deleted"



#Lägger till en ny recession på en extisterade bok 
@app.route("/book",methods = ["POST"])
def add_new_review():
    data = request.json
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO recensioner (bok_id, anvandare, betyg, recensionstext)
            VALUES (?, ?, ?, ?)""", 
            (data["bok_id"],data["anvandare"],data["betyg"],data["recensionstext"]))

    return "Recensionen är till lagd"


#Hämtar alla reccesioner på alla böcker 
@app.route("/all_reviews")
def get_reviews():
    with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM recensioner")
        all_reviews = cursor.fetchall()
    return jsonify({"recensioner": all_reviews})

#Hämtar alla resensioner på valda bokens ID
@app.route("/review/<int:bok_id>")
def get_all_reviews(bok_id):
     with sqlite3.connect("Bocker.db") as connection:
        cursor = connection.cursor()
        cursor.execute ("SELECT * FROM recensioner WHERE bok_id =?",(int(bok_id),))

        reviews = cursor.fetchall()

        return reviews
     
     
#Hämtar top 5 böcker i databasen baserad på betyg 
@app.route("/books/top")
def get_top_books ():
    with sqlite3.connect("Bocker.db") as con:
        cursor = con.cursor()
        cursor.execute("""
           SELECT bok.id, bok.titel, AVG(res.betyg) AS average_rating
            FROM bocker bok
            LEFT JOIN recensioner res ON bok.id = res.bok_id
            GROUP BY bok.id, bok.titel
            ORDER BY average_rating DESC
            LIMIT 5  
        """)
        result = cursor.fetchall()
        print(result)
        return result
    
#Hämtar informationen om författaren som man skriver in med hjälp av en api      
@app.route("/author")

def get_summry_of_author():
    get_author = request.args.get("author", None)
    data = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{get_author}")
    data = data.json()
    new_deta = data["extract"]
 
    return new_deta

#Hämtar top work från valda författaren 
@app.route("/top_work")
def get_top ():
    get_top = request.args.get("author",None)
    data = requests.get(f"https://openlibrary.org/search/authors.json?q={get_top}")
    data = data.json()

    top_work = data["docs"][0].get("top_work")
    

    return top_work


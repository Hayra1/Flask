**README**

This repository contains the code for a Flask-based web application designed to manage a book database. Users can perform various operations such as adding, updating, deleting books, as well as leaving reviews for books. The application also includes features such as searching for books, retrieving top-rated books, and fetching information about authors using external APIs.

**Getting Started**

1. Clone the repository to your local machine:

   ```
   git clone <repository_url>
   ```

2. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Ensure you have SQLite installed on your system.

4. Run the Flask application:

   ```
   python app.py
   ```

5. Access the application by navigating to `http://localhost:5000` in your web browser.

**Endpoints**

- **GET /** - Returns a simple "Hello!" message indicating that the server is running.

- **GET /all_books** - Retrieves all books from the database.

- **GET /books?id={book_id}&titel={book_title}&forfattare={author_name}** - Searches for books based on optional parameters such as book ID, title, and author.

- **POST /books** - Adds new books to the database. Requires JSON input containing book details.

- **PUT /update_books/{book_id}** - Updates the title of a book in the database.

- **DELETE /delete_book/{book_id}** - Deletes a book from the database.

- **POST /book** - Adds a new review for an existing book.

- **GET /all_reviews** - Retrieves all reviews from the database.

- **GET /review/{book_id}** - Retrieves all reviews for a specific book.

- **GET /books/top** - Retrieves the top 5 highest-rated books from the database.

- **GET /author** - Fetches information about an author using the Wikipedia API.

- **GET /top_work** - Retrieves the top work of a given author using the OpenLibrary API.

**Testing**

This project includes unit tests written using pytest. To run the tests, execute the following command:

```
pytest
```

The tests cover various endpoints and ensure that the application functions correctly under different scenarios.

**Database**

The application uses SQLite as its database. The database files (`Bocker.db`) are included in the project directory.

**Note:** Before running the application, ensure that the necessary database files exist and are accessible to the application.

Feel free to explore the codebase and make any modifications as needed. If you encounter any issues or have suggestions for improvements, please don't hesitate to open an issue or submit a pull request. Thank you!

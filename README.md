# Book Retrieval API
This project implements a RESTful API for a book retrieval system using Django and Django REST Framework (DRF). The API allows searching for books based on various filter criteria, supporting pagination, and returning books in JSON format.

# Project Overview
The Book Retrieval API provides the following functionality:

Retrieve Books: Search for books based on zero or more filter criteria.

# Filter Options:

Book ID (Project Gutenberg ID numbers)
Language
Mime-type
Topic (filters on "subject" or "bookshelf" or both)
Author
Title
API Response:

Number of books matching the criteria.
A list of book objects with detailed information:
Title of the book
Information about the author
Genre
Language
Subject(s)
Bookshelf(s)
Download links for the book in available formats (mime-types).
Pagination: Retrieve books in sets of 25 if the results exceed the limit.

# Features
Case-Insensitive Partial Matching:
Supports case-insensitive search for topics, authors, and titles.
Example: Searching for topic=child will return books with subjects like Child education and bookshelves like Children’s literature.
Multiple Filter Criteria:
Allows combining multiple filter criteria in a single API call.
Example: Filter on language=en,fr and topic=child,infant.

# Ensure you have the following installed:

Python 3.x
pip (Python package installer)
Django
Django REST Framework (DRF)
Steps to Run the Project
Clone the repository
Clone the project from GitHub:

# bash
Copy code
  
  git clone https://github.com/Nimapatel1234/books_api.git

  
cd book-api

Create a Virtual Environment

Set up a virtual environment to manage project dependencies:

# bash
Copy code
python -m venv venv



source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies


Install the required Python libraries using requirements.txt:

# bash
Copy code
pip install -r requirements.txt



Run Migrations



python manage.py makemigrations



Apply database migrations:

# bash
Copy code
python manage.py migrate

Start the Development Server 

Run the Django development server:

# bash
Copy code
python manage.py runserver

Install Swagger API for API Endpoint Documentation
To enable Swagger/OpenAPI documentation for your API endpoints, install the drf-yasg package:

bash
Copy code
pip install drf-yasg


Access the API
The API will be available at:


 # API Endpoints
Retrieve Books
Endpoint: /api/books/
Method: GET
Description: Retrieve books based on filter criteria.
Query Parameters
Parameter	Type	Description	Example
id	Integer	Filter by Project Gutenberg book ID.	id=1234
language	String	Filter by language. Multiple values can be provided.	language=en,fr
mime-type	String	Filter by mime-type of download formats.	mime-type=text/plain
topic	String	Filter by subject or bookshelf. Supports partial matches.	topic=child
author	String	Filter by author's name. Supports case-insensitive partial matching.	author=shakespeare
title	String	Filter by book title. Supports case-insensitive partial matching.	title=hamlet
page	Integer	Paginate through results (25 books per page).	page=2


Response Example
json
{
    "count": 6,
    "next": null,
    "previous": null,
    "results": [
       
       
        {
            "id": 11,
            "title": "another example",
            "author_name": "john doe",
            "genre": "fiction",
            "language": "English",
            "subject": "children's literature",
            "bookshelf": "child education",
            "download_count": 10,
            "download_links": []
        },
        {
            "id": 1,
            "title": "swdefg",
            "author_name": "1",
            "genre": "sdfvgbn",
            "language": "sxdcvb",
            "subject": "sdcfvb n",
            "bookshelf": null,
            "download_count": 0,
            "download_links": [
                {
                    "mime_type": "application/octet-stream",
                    "url": "https://workdrive.zohoexternal.com/file/tkojn5916f1c21d994f5da21158f29d5b186a"
                }
            ]
        }
    ]
}


# Pagination
The API supports pagination for GET requests to the

/api/books/ endpoint. By default, 10 items are returned per page.


Example


http://127.0.0.1:8000/api/books/?page=2&page_size=4

Example API Call
To retrieve books in English or French related to "child" or "infant" topics:

Copy code
GET /api/books/?language=en,fr&topic=child,infant


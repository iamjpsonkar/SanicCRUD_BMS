from sanic import Sanic
from sanic.response import json, html, HTTPResponse
from sanic.views import HTTPMethodView

app = Sanic(__name__)

BOOKS = {
    "1":{
        "book_id": 1,
        "title": "title1",
        "author": "author1",
        "published_date": "10/11/2021"
    },
    "2":{
        "book_id": 2,
        "title": "title2",
        "author": "author2",
        "published_date": "10/11/2021"
    },
    "3":{
        "book_id": 3,
        "title": "title3",
        "author": "author3",
        "published_date": "10/11/2021"
    },
}

class Home(HTTPMethodView):
    async def get(self, request):
        html_content = """
            <html>
                <head>
                    <title>Book Management System</title>
                </head>
                <body>
                    <h1>Welcome to Book Management System</h1>
                    <a href="/books/"> Get All Books </a>
                </body>
            </html>
        """
        return html(html_content)


class BookManagementSystem(HTTPMethodView):
    async def get(self, request,*args, **kwargs):
        book_id = kwargs.get("book_id")
        if book_id:
            if BOOKS.get(str(book_id)):
                return json(BOOKS.get(str(book_id)))
            else:
                return json({"status":400, "message":"book not found"})
        else:
            return json(BOOKS)

    async def post(self, request,*args, **kwargs):
        book_id = kwargs.get("book_id")
        book = request.json
        if book:
            if book.get('book_id') not in BOOKS:
                BOOKS[str(book.get('book_id'))] = book
                return json({"status":200, "message":"book added successfully"})
            else:
                return json({"status":500, "message":"book already exist"})
        else:
            return json({"status":400, "message":"Invalid book"})

    async def put(self, request,*args, **kwargs):
        book_id = kwargs.get("book_id")
        book = request.json
        if book_id and book:
            if BOOKS.get(str(book_id)):
                BOOKS[str(book_id)] ={
                    "title": book.get("title",BOOKS.get(str(book_id),{}).get("title")),
                    "author": book.get("author",BOOKS.get(str(book_id),{}).get("author")),
                    "published_date": book.get("published_date",BOOKS.get(str(book_id),{}).get("published_date")),
                }
                return json({"status":200, "message":"book updated successfully!"})
            else:
                return json({"status":400, "message":"book not found!"})
        else:
            return json({"status":500, "message":"Invalid Data!"})

    async def delete(self, request,*args, **kwargs):
        book_id = kwargs.get("book_id")
        if book_id and BOOKS.get(str(book_id)):
                del BOOKS[str(book_id)]
                return json({"status":200, "message":"book deleted successfully!"})
        else:
            return json({"status":400, "message":"book not found!"})


app.add_route(Home.as_view(),"/",methods=["GET"], name="home_view")

book_view = BookManagementSystem.as_view()

app.add_route(book_view, "/books/<book_id>/", methods=[ "GET", "PUT", "DELETE"], name="book_d")
app.add_route(book_view, "/books", methods=["GET", "POST"], name="book_view")

if __name__ == '__main__':
    app.run(debug=True, auto_reload=True)
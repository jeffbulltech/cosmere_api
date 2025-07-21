from fastapi import FastAPI

app = FastAPI()

@app.get("/api/v1/books")
def get_books():
    return [
        {"id": "test-book", "title": "Test Book", "world_id": "roshar"}
    ]

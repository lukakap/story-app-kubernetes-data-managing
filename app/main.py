from fastapi import FastAPI, HTTPException, Response, status
from typing import Dict
import os

app = FastAPI()

FILE_PATH = f"{os.getenv('STORY_FOLDER')}/file.txt"

@app.get("/story")
def get_story() -> str:
    try:
        with open(FILE_PATH, "r") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")

@app.post("/story")
def post_story(data: Dict[str, str]) -> Response:
    new_text = data.get("text")
    if not new_text:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No text provided")
    try:
        with open(FILE_PATH, "a") as f:
            f.write("\n" + new_text)
    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="File not found")
    return Response(status_code=status.HTTP_201_CREATED)

@app.get("/error")
def crash_app():
    # Raise an exception to crash the application
    os._exit(1)
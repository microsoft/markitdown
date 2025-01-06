import pytest
from fastapi.testclient import TestClient
from markitdown.api import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the MarkItDown API"}

def test_convert_success():
    with open("tests/test_files/test.docx", "rb") as file:
        response = client.post("/convert", files={"file": file})
    assert response.status_code == 200
    assert "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation" in response.json()["text_content"]

def test_convert_unsupported_format():
    with open("tests/test_files/test.unsupported", "rb") as file:
        response = client.post("/convert", files={"file": file})
    assert response.status_code == 400
    assert response.json() == {"detail": "Unsupported file format"}

def test_convert_conversion_error():
    with open("tests/test_files/test_corrupted.docx", "rb") as file:
        response = client.post("/convert", files={"file": file})
    assert response.status_code == 500
    assert response.json() == {"detail": "File conversion error"}

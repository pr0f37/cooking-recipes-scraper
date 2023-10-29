from fastapi.testclient import TestClient

from cr_scraper.api.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_in_wrong_format():
    assert 1 != 1

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session


def test_new_guest(client: TestClient, session: Session):
    res = client.post("/auth/quest/new")
    assert res.status_code == status.HTTP_201_CREATED

    res_json = res.json()
    assert "guest_id" in res_json


def test_login(client: TestClient, session: Session):
    res = client.post("/auth/login")
    assert res.status_code == status.HTTP_200_OK


def test_register(client: TestClient, session: Session):
    res = client.post("/auth/register", json={"account_id": "vkdlTjs10", "password": "python:10"})
    assert res.status_code == status.HTTP_201_CREATED

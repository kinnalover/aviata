import json

from fastapi import status
from sqlalchemy.testing import db
from db.repository.searches import get_seach_by_id
from db.repository.searches import update_search
from schemas.searches import SearchUpdate


def test_provider_a(client):
    response =client.post("/provider-a/search")
    print(response.status_code)
    assert response.status_code ==200


def test_provider_b(client):
    response =client.post("/provider-b/search")
    print(response.status_code)
    assert response.status_code ==200


def test_airflow_search(client):
    response = client.post("/airflow/search")
    assert response.status_code == 200
    assert "search_id" in response.json()








def test_airflow_search_results(client):
    response = client.post("/airflow/search")
    search_id=response.json()['search_id']
    currency="KZT"
    response =client.post(f"/airflow/results/{search_id}/{currency}")
    print(response.status_code)
    assert response.status_code ==200

import pytest

def test_get_movies_unauthorized(client):
	response = client.get("/movies/all_movies")
	assert response.status_code == 401


def test_get_movies_authorized(client, user_data):
	client.post("/auth/register", json=user_data)
	login = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "password123"
	})
	token = login.json()["access_token"]

	response = client.get("/movies/all_movies", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert isinstance(response.json(), list)
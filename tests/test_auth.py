import pytest


def test_register_success(client, user_data):
	response = client.post("/auth/register", json=user_data)
	assert response.status_code == 201
	data = response.json()
	assert data["email"] == "test@test.com"
	assert "password" not in data 


def test_register_duplicate_email(client, user_data):
	client.post("/auth/register", json=user_data)
	response = client.post("/auth/register", json=user_data)
	assert response.status_code == 400


def test_login_success(client, user_data):
	client.post("/auth/register", json=user_data)
	response = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "password123"
	})
	assert response.status_code == 200
	data = response.json()
	assert "access_token" in data


def test_login_wrong_password(client, user_data):
	client.post("/auth/register", json=user_data)
	response = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "wrongpassword"
	})
	assert response.status_code == 401


def test_logout_success(client, user_data):
	client.post("/auth/register", json=user_data)
	login = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "password123"
	})
	token = login.json()["access_token"]
	response = client.post(
		"/auth/logout",
		headers={"Authorization": f"Bearer {token}"}
	)
	assert response.status_code == 200
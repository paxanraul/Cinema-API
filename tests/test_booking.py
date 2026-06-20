def test_get_bookings(client, user_data):
	client.post("/auth/register", json=user_data)
	login = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "password123"
	})
	token = login.json()["access_token"]

	response = client.get("/bookings/all_my_bookings", headers={"Authorization": f"Bearer {token}"})
	assert response.status_code == 200
	assert isinstance(response.json(), list)


def test_create_booking(client, user_data):
	client.post("/auth/register", json=user_data)
	login = client.post("/auth/login", json={
		"email": "test@test.com",
		"password": "password123"
	})
	token = login.json()["access_token"]
	headers = {"Authorization": f"Bearer {token}"}

	movie = client.post("/movies/create_movie", json={
		"name": "Тест",
		"year": 2026,
		"description": "Описание",
		"duration_minutes": 120,
		"genre": "Crime",
		"director": "Иванов"
	}, headers=headers)
	movie_id = movie.json()["id"]

	hall = client.post("/halls/create_hall", json={
		"name": "Зал 1",
		"capacity": 100,
		"location": "Этаж 1"
	}, headers=headers)
	hall_id = hall.json()["id"]

	session = client.post("/sessions/create_session", json={
		"movie_id": movie_id,
		"hall_id": hall_id,
		"start_time": "2030-01-01T20:00:00+00:00"
	}, headers=headers)
	session_id = session.json()["id"]

	response = client.post("/bookings/create_booking",
		json={
			"session_id": session_id
		}, headers=headers)
	assert response.status_code == 201
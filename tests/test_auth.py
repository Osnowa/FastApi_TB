async def test_register_user(client):
    response = await client.post(
    "/auth/register",
    json={
        "email": "ilaM4@example.com",
        "password": "test_password"
    }
    )
    assert response.status_code == 201

async def test_login_user(client):
    await client.post(
        "/auth/register",
        json={
            "email": "ilaM4@example.com", 
            "password": "test_password"
            }
        )  # Регистрируем пользователя перед тестом логина

    response = await client.post(
    "/auth/login",
    json={
        "email": "ilaM4@example.com",
        "password": "test_password"
    }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
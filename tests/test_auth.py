async def test_register_user(client):
    response = await client.post(
    "/auth/register",
    json={
        "email": "ilaM4@example.com",
        "password": "test_password"
    }
    )
    assert response.status_code == 201

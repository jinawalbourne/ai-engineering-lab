def test_health_returns_healthy_when_database_is_available(
    client, monkeypatch
):
    monkeypatch.setattr("app.main.check_database_connection", lambda: True)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_health_returns_unhealthy_when_database_is_unavailable(
    client, monkeypatch
):
    monkeypatch.setattr("app.main.check_database_connection", lambda: False)

    response = client.get("/health")

    assert response.status_code == 503
    assert response.json() == {"status": "unhealthy"}

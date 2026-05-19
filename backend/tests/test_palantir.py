from unittest.mock import AsyncMock, patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scrape_requires_auth(client):
    response = client.post("/api/scrape", json={"url": "https://example.com"})
    assert response.status_code in (401, 403)


def test_scrape_creates_job(client, auth_headers):
    with (
        patch("routes.scrape.robots_check.check", return_value="allowed"),
        patch("routes.scrape.outline_gen.generate", new_callable=AsyncMock,
              return_value="# Outline: Test\n## Summary\nTest content."),
    ):
        response = client.post(
            "/api/scrape",
            json={"url": "https://example.com"},
            headers=auth_headers,
        )
    assert response.status_code == 200
    data = response.json()
    assert "job_id" in data
    assert data["status"] == "pending"


def test_get_job(client, auth_headers):
    with (
        patch("routes.scrape.robots_check.check", return_value="allowed"),
        patch("routes.scrape.outline_gen.generate", new_callable=AsyncMock,
              return_value="# Outline: Test\n## Summary\nTest content."),
    ):
        create_resp = client.post(
            "/api/scrape",
            json={"url": "https://example.com"},
            headers=auth_headers,
        )
    job_id = create_resp.json()["job_id"]

    response = client.get(f"/api/jobs/{job_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["status"] in ("pending", "running", "done", "error")

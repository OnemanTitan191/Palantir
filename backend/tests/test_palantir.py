from pathlib import Path
from unittest.mock import AsyncMock, patch


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_scrape_requires_auth(client):
    response = client.post("/api/scrape", json={"url": "https://example.com"})
    assert response.status_code == 401


def test_jobs_requires_auth(client):
    assert client.get("/api/jobs").status_code == 401
    assert client.get("/api/jobs/1").status_code == 401


def test_outlines_requires_auth(client):
    assert client.get("/api/outlines").status_code == 401
    assert client.get("/api/outlines/1").status_code == 401


def test_scrape_creates_job(client, auth_headers):
    with (
        patch("routes.scrape.robots_check.check", return_value="allowed"),
        patch("routes.scrape.outline_gen.generate", new_callable=AsyncMock,
              return_value="# Outline: Test\n## Summary\nTest content."),
        patch("routes.scrape.storage.write_md", return_value=Path("/tmp/2026-05-19_test.md")),
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


def test_scrape_invalid_url(client, auth_headers):
    response = client.post(
        "/api/scrape",
        json={"url": "not-a-url"},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_get_job(client, auth_headers):
    with (
        patch("routes.scrape.robots_check.check", return_value="allowed"),
        patch("routes.scrape.outline_gen.generate", new_callable=AsyncMock,
              return_value="# Outline: Test\n## Summary\nTest content."),
        patch("routes.scrape.storage.write_md", return_value=Path("/tmp/2026-05-19_test.md")),
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


def test_get_job_not_found(client, auth_headers):
    response = client.get("/api/jobs/9999", headers=auth_headers)
    assert response.status_code == 404


def test_list_outlines_empty(client, auth_headers):
    response = client.get("/api/outlines", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_get_outline_not_found(client, auth_headers):
    response = client.get("/api/outlines/9999", headers=auth_headers)
    assert response.status_code == 404

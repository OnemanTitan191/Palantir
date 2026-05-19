import os
import tempfile

_outputs_tmp = tempfile.mkdtemp()

# Set env vars before any app module is imported
os.environ["PALANTIR_SECRET"] = "test-secret"
os.environ["USE_MOCK_FIRECRAWL"] = "true"
os.environ["ANTHROPIC_API_KEY"] = "test-key"
os.environ["PALANTIR_OUTPUTS_DIR"] = _outputs_tmp

import pytest
from sqlalchemy import create_engine, event as sa_event
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

import database

_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
_test_engine = create_engine(
    f"sqlite:///{_tmp.name}", connect_args={"check_same_thread": False}
)

@sa_event.listens_for(_test_engine, "connect")
def _pragmas(conn, _):
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")

database.engine = _test_engine
database.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

from main import app
from database import Base, get_db

# load_dotenv(override=True) in main.py overwrites test env vars; re-apply them here
os.environ["PALANTIR_SECRET"] = "test-secret"
os.environ["USE_MOCK_FIRECRAWL"] = "true"


def _override_get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=_test_engine)
    yield
    Base.metadata.drop_all(bind=_test_engine)


@pytest.fixture(scope="session", autouse=True)
def cleanup_tmp_db():
    yield
    try:
        os.unlink(_tmp.name)
    except OSError:
        pass


@pytest.fixture
def client(reset_db):
    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-secret"}

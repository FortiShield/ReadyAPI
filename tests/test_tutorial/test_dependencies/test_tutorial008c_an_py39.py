import pytest
from readyapi.exceptions import ReadyAPIError
from readyapi.testclient import TestClient

from ...utils import needs_py39


@pytest.fixture(name="client")
def get_client():
    from docs_src.dependencies.tutorial008c_an_py39 import app

    client = TestClient(app)
    return client


@needs_py39
def test_get_no_item(client: TestClient):
    response = client.get("/items/foo")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Item not found, there's only a plumbus here"}


@needs_py39
def test_get(client: TestClient):
    response = client.get("/items/plumbus")
    assert response.status_code == 200, response.text
    assert response.json() == "plumbus"


@needs_py39
def test_readyapi_error(client: TestClient):
    with pytest.raises(ReadyAPIError) as exc_info:
        client.get("/items/portal-gun")
    assert "No response object was returned" in exc_info.value.args[0]


@needs_py39
def test_internal_server_error():
    from docs_src.dependencies.tutorial008c_an_py39 import app

    client = TestClient(app, raise_server_exceptions=False)
    response = client.get("/items/portal-gun")
    assert response.status_code == 500, response.text
    assert response.text == "Internal Server Error"

import pytest
import aiohttp
from unittest.mock import AsyncMock, MagicMock
from app.core.third_party_integrations.manychat.client import ManyChatClient

@pytest.fixture
def mock_config():
    class MockConfig:
        api_key = "test_api_key"
        base_url = "https://api.manychat.com"
        timeout = 30
        max_retries = 3
    return MockConfig()

@pytest.fixture
async def mock_client(mock_config):
    async with aiohttp.ClientSession() as session:
        client = ManyChatClient(config=mock_config)
        client._session = session
        yield client
        await client.close()

@pytest.fixture
def mock_http_client(monkeypatch):
    mock_session = AsyncMock()
    mock_response = AsyncMock()
    mock_response.json = AsyncMock(return_value={"status": "success"})
    mock_session.request.return_value.__aenter__.return_value = mock_response
    
    client = ManyChatClient(api_key="test_api_key")
    monkeypatch.setattr(client, "_session", mock_session)
    return client, mock_session, mock_response
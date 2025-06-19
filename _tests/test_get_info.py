import pytest
from app.core.third_party_integrations.manychat.api.facebook.getInfo import get_page_info
from app.core.third_party_integrations.manychat.api.facebook._responses import PageInfoResponse

@pytest.mark.asyncio
async def test_get_page_info_success(mock_http_client):
    client, mock_session, mock_response = mock_http_client
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "id": 12345,
            "name": "Test Page",
            "category": "Test Category",
            "is_pro": True
        }
    }
    
    result = await get_page_info(client)
    
    assert isinstance(result, PageInfoResponse)
    assert result.status == "success"
    assert result.data.id == 12345
    assert result.data.name == "Test Page"
    mock_session.request.assert_awaited_once_with(
        "GET",
        "https://api.manychat.com/fb/page/getInfo",
        headers={"Authorization": "Bearer test_api_key"},
        json=None
    )
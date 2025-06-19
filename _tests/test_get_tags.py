import pytest
from app.core.third_party_integrations.manychat.api.facebook.getTags import get_tags
from app.core.third_party_integrations.manychat.api.facebook._responses import TagsListResponse

@pytest.mark.asyncio
async def test_get_tags_success(mock_http_client):
    client, mock_session, mock_response = mock_http_client
    mock_response.json.return_value = {
        "status": "success",
        "data": [
            {"id": 1, "name": "Tag 1"},
            {"id": 2, "name": "Tag 2"}
        ]
    }
    
    result = await get_tags(client)
    
    assert isinstance(result, TagsListResponse)
    assert result.status == "success"
    assert len(result.data) == 2
    mock_session.request.assert_awaited_once_with(
        "GET",
        "https://api.manychat.com/fb/page/getTags",
        headers={"Authorization": "Bearer test_api_key"},
        json=None
    )
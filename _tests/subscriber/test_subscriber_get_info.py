import pytest
from datetime import datetime
from app.core.third_party_integrations.manychat.api.facebook.subscriber.getInfo import get_subscriber_info
from app.core.third_party_integrations.manychat.api.facebook.subscriber._responses import GetSubscriberInfoResponse

@pytest.mark.asyncio
async def test_get_subscriber_info_success(mock_http_client):
    client, mock_session, mock_response = mock_http_client
    mock_response.json.return_value = {
        "status": "success",
        "data": {
            "id": "12345",
            "page_id": "67890",
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "tags": [{"id": 1, "name": "VIP"}]
        }
    }
    
    result = await get_subscriber_info(
        client,
        subscriber_id="12345",
        fields=["first_name", "last_name", "email"]
    )
    
    assert isinstance(result, GetSubscriberInfoResponse)
    assert result.status == "success"
    assert result.data.id == "12345"
    assert result.data.first_name == "John"
    assert len(result.data.tags) == 1
    mock_session.request.assert_awaited_once_with(
        "GET",
        "https://api.manychat.com/fb/subscriber/getInfo",
        headers={"Authorization": "Bearer test_api_key"},
        params={
            "subscriber_id": "12345",
            "fields": ["first_name", "last_name", "email"]
        }
    )
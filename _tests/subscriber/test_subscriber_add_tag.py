import pytest
from app.core.third_party_integrations.manychat.api.facebook.subscriber.addTagByName import add_tag_by_name
from app.core.third_party_integrations.manychat.api._responses import SuccessResponse

@pytest.mark.asyncio
async def test_add_tag_by_name_success(mock_http_client):
    client, mock_session, mock_response = mock_http_client
    mock_response.json.return_value = {"status": "success"}
    
    result = await add_tag_by_name(
        client,
        subscriber_id="12345",
        tag_name="VIP"
    )
    
    assert isinstance(result, SuccessResponse)
    assert result.status == "success"
    mock_session.request.assert_awaited_once_with(
        "POST",
        "https://api.manychat.com/fb/subscriber/addTagByName",
        headers={"Authorization": "Bearer test_api_key"},
        json={"subscriber_id": "12345", "tag_name": "VIP"}
    )
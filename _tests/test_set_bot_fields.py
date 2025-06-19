import pytest
from app.core.third_party_integrations.manychat.api.facebook.setBotFields import set_bot_fields
from app.core.third_party_integrations.manychat.api.facebook._responses import SetBotFieldsResponse

@pytest.mark.asyncio
async def test_set_bot_fields_success(mock_http_client):
    client, mock_session, mock_response = mock_http_client
    mock_response.json.return_value = {
        "status": "success",
        "data": [
            {"field_id": 1, "success": True},
            {"field_name": "test", "success": True}
        ]
    }
    
    fields = [
        {"field_id": 1, "field_value": "test"},
        {"field_name": "test", "field_value": 123}
    ]
    
    result = await set_bot_fields(client, fields)
    
    assert isinstance(result, SetBotFieldsResponse)
    assert result.status == "success"
    assert len(result.data) == 2
    mock_session.request.assert_awaited_once_with(
        "POST",
        "https://api.manychat.com/fb/page/setBotFields",
        headers={"Authorization": "Bearer test_api_key"},
        json={"fields": fields}
    )
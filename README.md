# ManyChat Python SDK: Async API Client for ManyChat

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI version](https://badge.fury.io/py/manychat-sdk.svg)](https://badge.fury.io/py/manychat-sdk)

A high-performance, fully asynchronous Python SDK for the ManyChat API. Built with modern Python practices, type safety, and developer experience in mind. Perfect for building scalable chatbots, automation workflows, and marketing tools.

## 🚀 Key Features

- **100% Asynchronous** – Built with `asyncio` for maximum performance  
- **Type Safe** – Full type hints and Pydantic validation  
- **Production Ready** – Battle-tested in high-traffic environments  
- **Complete API Coverage** – All ManyChat endpoints implemented  
- **Developer Friendly** – Intuitive API design with detailed documentation  

## 📦 Installation

```bash
pip install manychat-sdk
# or with poetry
poetry add manychat-sdk
📚 Documentation
Full Documentation

API Reference

💡 Quick Start
1. Initialize Client
python
Copy
Edit
from manychat import ManyChatClient

async def main():
    async with ManyChatClient(api_key="your_api_key") as client:
        # Start using the client
        ...
2. Get Page Information
python
Copy
Edit
from manychat.api.facebook import get_page_info
from manychat import ManyChatClient

async def show_page_info():
    async with ManyChatClient() as client:
        page = await get_page_info(client)
        print(f"Page: {page.data.name}")
        print(f"Category: {page.data.category}")
3. Manage Subscribers
python
Copy
Edit
from manychat.api.facebook.subscriber import get_subscriber_info, add_tag_by_name
from manychat import ManyChatClient

async def tag_vip_customer(subscriber_id: str):
    async with ManyChatClient() as client:
        # Get subscriber details
        subscriber = await get_subscriber_info(client, subscriber_id=subscriber_id)
        
        # Add VIP tag
        await add_tag_by_name(
            client,
            subscriber_id=subscriber_id,
            tag_name="VIP"
        )
🔄 API Endpoints
Facebook API
get_page_info() – Get page details and statistics

get_tags() – List all available tags

set_bot_fields() – Update bot configuration

Subscriber Management
get_subscriber_info() – Retrieve subscriber details

add_tag_by_name() – Tag subscribers

remove_tag() – Remove tags

set_custom_field() – Update subscriber fields

🛠️ Advanced Usage
Error Handling
python
Copy
Edit
from manychat.exceptions import ManyChatRateLimitError, ManyChatAPIError
from manychat import ManyChatClient
from manychat.api.facebook import get_page_info

async def safe_call():
    try:
        async with ManyChatClient() as client:
            await get_page_info(client)
    except ManyChatRateLimitError as e:
        print(f"Rate limited! Try again in {e.retry_after} seconds")
    except ManyChatAPIError as e:
        print(f"API Error: {e}")
Configuration Options
python
Copy
Edit
from manychat import ManyChatConfig

config = ManyChatConfig(
    api_key="your_api_key",
    timeout=30,         # seconds
    max_retries=3,
    base_url="https://api.manychat.com"
)
🧪 Testing
bash
Copy
Edit
# Run tests
pytest tests/ -v

# With coverage
pytest --cov=manychat tests/
🤝 Contributing
We welcome contributions! Please see our Contributing Guide for details.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.
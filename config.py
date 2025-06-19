from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class ManyChatConfig(BaseSettings):
    """Configuration for ManyChat API integration.
    
    Loads configuration from environment variables with the prefix 'MANYCHAT_'.
    """
    model_config = SettingsConfigDict(env_prefix="MANYCHAT_", env_file=".env", extra="ignore")
    
    # Required configuration
    api_key: str = Field(..., description="API key for ManyChat authentication")
    api_version: str = Field("v1", description="API version to use")
    base_url: str = Field("https://api.manychat.com/fb", 
                         description="Base URL for ManyChat API endpoints")
    
    # Optional configuration with defaults
    timeout: int = Field(30, description="Request timeout in seconds")
    max_retries: int = Field(3, description="Maximum number of retries for failed requests")
    retry_delay: float = Field(1.0, description="Delay between retries in seconds")
    
    # Rate limiting
    rate_limit: int = Field(100, description="Maximum requests per minute")
    rate_window: int = Field(60, description="Rate limit window in seconds")
    
    # Logging and debugging
    log_level: str = Field("INFO", description="Logging level")
    debug: bool = Field(False, description="Enable debug mode for additional logging")
    
    # Webhook configuration
    webhook_secret: Optional[str] = Field(
        None, 
        description="Secret for webhook signature verification"
    )
    
    # Cache settings
    cache_ttl: int = Field(300, description="Default cache TTL in seconds")
    
    @property
    def api_url(self) -> str:
        """Get the full base API URL with version."""
        return f"{self.base_url}/{self.api_version}"


# Create a singleton instance
config = ManyChatConfig()

__all__ = ["config", "ManyChatConfig"]

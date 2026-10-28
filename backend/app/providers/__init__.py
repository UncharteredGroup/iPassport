"""Model provider interface + selection (mock vs live Meta Model API)."""

from .base import Provider
from .mock import MockProvider

__all__ = ["Provider", "MockProvider", "get_provider"]

_provider: Provider | None = None


def get_provider() -> Provider:
    """Return the configured provider (mock by default, live when configured)."""
    global _provider
    if _provider is not None:
        return _provider
    from app.config import get_settings

    settings = get_settings()
    if not settings.mock_mode and settings.meta_api_key:
        from .meta_api import MetaApiProvider

        _provider = MetaApiProvider(
            api_base=settings.meta_api_base,
            api_key=settings.meta_api_key,
            agent_model=settings.meta_agent_model,
            vision_model=settings.meta_vision_model,
            image_model=settings.meta_image_model,
        )
    else:
        _provider = MockProvider()
    return _provider

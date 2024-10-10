from tests.marks import pydantic_v2
from tests.mocks import mock_pydantic_settings_env


@pydantic_v2
def test_exists_and_valid() -> None:
    with mock_pydantic_settings_env({"url": "localhost:9092"}):
        from docs.docs_src.getting_started.config.settings_base_2 import settings

        assert settings.queue == "test-queue"
        assert settings.url == "localhost:9092"

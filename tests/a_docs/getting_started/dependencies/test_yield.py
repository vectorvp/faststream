import pytest

from faststream import TestApp
from tests.marks import require_aiokafka


@pytest.mark.asyncio()
@require_aiokafka
async def test_yield_kafka() -> None:
    from docs.docs_src.getting_started.dependencies.yield_kafka import (
        app,
        broker,
        handle,
    )
    from faststream.kafka import TestKafkaBroker

    async with TestKafkaBroker(broker), TestApp(app):
        handle.mock.assert_called_once_with("")

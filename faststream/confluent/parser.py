from typing import TYPE_CHECKING, Any, Optional, Tuple

from confluent_kafka import Message

from faststream.broker.message import StreamMessage, decode_message, gen_cor_id
from faststream.confluent.message import FAKE_CONSUMER, KafkaMessage
from faststream.types import DecodedMessage
from faststream.utils.context.repository import context

if TYPE_CHECKING:
    from faststream.confluent.subscriber.usecase import LogicSubscriber


class AsyncConfluentParser:
    """A class to parse Kafka messages."""

    @staticmethod
    async def parse_message(
        message: Message,
    ) -> StreamMessage[Message]:
        """Parses a Kafka message."""
        headers = {}
        if message.headers() is not None:
            for i, j in message.headers():  # type: ignore[union-attr]
                if isinstance(j, str):
                    headers[i] = j
                else:
                    headers[i] = j.decode()
        body = message.value()
        offset = message.offset()
        _, timestamp = message.timestamp()

        handler: Optional["LogicSubscriber[Any]"] = context.get_local("handler_")
        return KafkaMessage(
            body=body,
            headers=headers,
            reply_to=headers.get("reply_to", ""),
            content_type=headers.get("content-type"),
            message_id=f"{offset}-{timestamp}",
            correlation_id=headers.get("correlation_id", gen_cor_id()),
            raw_message=message,
            consumer=getattr(handler, "consumer", None) or FAKE_CONSUMER,
            is_manual=getattr(handler, "is_manual", True),
        )

    @staticmethod
    async def parse_message_batch(
        message: Tuple[Message, ...],
    ) -> StreamMessage[Tuple[Message, ...]]:
        """Parses a batch of messages from a Kafka consumer."""
        first = message[0]
        last = message[-1]

        headers = {}
        if first.headers() is not None:
            for i, j in first.headers():  # type: ignore[union-attr]
                if isinstance(j, str):
                    headers[i] = j
                else:
                    headers[i] = j.decode()
        body = [m.value() for m in message]
        first_offset = first.offset()
        last_offset = last.offset()
        _, first_timestamp = first.timestamp()

        handler: Optional["LogicSubscriber[Any]"] = context.get_local("handler_")
        return KafkaMessage(
            body=body,
            headers=headers,
            reply_to=headers.get("reply_to", ""),
            content_type=headers.get("content-type"),
            message_id=f"{first_offset}-{last_offset}-{first_timestamp}",
            correlation_id=headers.get("correlation_id", gen_cor_id()),
            raw_message=message,
            consumer=getattr(handler, "consumer", None) or FAKE_CONSUMER,
            is_manual=getattr(handler, "is_manual", True),
        )

    @staticmethod
    async def decode_message(msg: StreamMessage[Message]) -> DecodedMessage:
        """Decodes a message."""
        return decode_message(msg)

    @classmethod
    async def decode_message_batch(
        cls, msg: StreamMessage[Tuple[Message, ...]]
    ) -> DecodedMessage:
        """Decode a batch of messages."""
        return [decode_message(await cls.parse_message(m)) for m in msg.raw_message]
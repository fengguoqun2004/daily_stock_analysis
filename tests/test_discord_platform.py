# -*- coding: utf-8 -*-
import json
import time
from types import SimpleNamespace
from unittest.mock import patch

from nacl.signing import SigningKey

from bot.models import ChatType
from bot.platforms.discord import DiscordPlatform


def _make_platform(public_key: str) -> DiscordPlatform:
    with patch(
        "src.config.get_config",
        return_value=SimpleNamespace(
            discord_interactions_public_key=public_key,
        ),
    ):
        return DiscordPlatform()


def _current_timestamp() -> str:
    """返回当前 Unix 秒字符串，用于生成有效签名。"""
    return str(int(time.time()))


def _sign_headers(signing_key: SigningKey, body: bytes, timestamp: str | None = None):
    if timestamp is None:
        timestamp = _current_timestamp()
    signature = signing_key.sign(timestamp.encode("utf-8") + body).signature.hex()
    return {
        "X-Signature-Ed25519": signature,
        "X-Signature-Timestamp": timestamp,
    }


def test_signed_ping_request_is_accepted():
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {"type": 1}
    body = json.dumps(payload).encode("utf-8")

    message, response = platform.handle_webhook(
        _sign_headers(signing_key, body),
        body,
        payload,
    )

    assert message is None
    assert response is not None
    assert response.status_code == 200
    assert response.body == {"type": 1}


def test_signed_interaction_request_is_parsed():
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {
        "id": "interaction-1",
        "type": 2,
        "channel_id": "channel-1",
        "guild_id": "guild-1",
        "member": {
            "user": {
                "id": "user-1",
                "username": "tester",
            }
        },
        "data": {
            "name": "analyze",
            "options": [
                {"name": "stock_code", "value": "600519"},
            ],
        },
    }
    body = json.dumps(payload).encode("utf-8")

    message, response = platform.handle_webhook(
        _sign_headers(signing_key, body),
        body,
        payload,
    )

    assert response is None
    assert message is not None
    assert message.platform == "discord"
    assert message.chat_id == "channel-1"
    assert message.chat_type == ChatType.GROUP
    assert message.user_id == "user-1"
    assert message.user_name == "tester"
    assert message.content == "/analyze 600519"


def test_invalid_signature_ping_request_is_rejected_before_challenge():
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {"type": 1}
    body = json.dumps(payload).encode("utf-8")
    headers = _sign_headers(signing_key, body)
    headers["X-Signature-Ed25519"] = "00" * 64

    message, response = platform.handle_webhook(headers, body, payload)

    assert message is None
    assert response is not None
    assert response.status_code == 401
    assert response.body == {"error": "Invalid Discord signature"}


def test_missing_signature_header_is_rejected():
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {
        "id": "interaction-2",
        "type": 2,
        "data": {"name": "help"},
    }
    body = json.dumps(payload).encode("utf-8")

    message, response = platform.handle_webhook(
        {"X-Signature-Timestamp": _current_timestamp()},
        body,
        payload,
    )

    assert message is None
    assert response is not None
    assert response.status_code == 401
    assert response.body == {"error": "Invalid Discord signature"}


def test_invalid_public_key_configuration_is_rejected():
    platform = _make_platform("not-a-hex-public-key")
    payload = {"type": 1}
    body = json.dumps(payload).encode("utf-8")

    message, response = platform.handle_webhook(
        {
            "X-Signature-Ed25519": "00" * 64,
            "X-Signature-Timestamp": _current_timestamp(),
        },
        body,
        payload,
    )

    assert message is None
    assert response is not None
    assert response.status_code == 401
    assert response.body == {"error": "Invalid Discord signature"}


def test_expired_timestamp_is_rejected():
    """过期 timestamp（超出 ±5 分钟窗口）应被拒绝，防重放攻击。"""
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {"type": 1}
    body = json.dumps(payload).encode("utf-8")
    # 10 分钟前的 timestamp
    stale_ts = str(int(time.time()) - 600)

    message, response = platform.handle_webhook(
        _sign_headers(signing_key, body, timestamp=stale_ts),
        body,
        payload,
    )

    assert message is None
    assert response is not None
    assert response.status_code == 401


def test_format_response_wraps_interaction_callback():
    """type=2 交互响应应使用 Interaction Response 回调格式（type=4 + data）。"""
    from bot.models import BotMessage, BotResponse, ChatType

    platform = _make_platform("00" * 32)
    message = BotMessage(
        platform="discord",
        message_id="msg-1",
        user_id="user-1",
        user_name="tester",
        chat_id="channel-1",
        chat_type=ChatType.GROUP,
        content="/analyze 600519",
        raw_data={"type": 2, "data": {"name": "analyze"}},
    )
    response = BotResponse.text_response("分析结果")

    webhook_response = platform.format_response(response, message)

    assert webhook_response.status_code == 200
    assert webhook_response.body["type"] == 4
    assert "data" in webhook_response.body
    assert webhook_response.body["data"]["content"] == "分析结果"
    assert webhook_response.body["data"]["tts"] is False


def test_non_numeric_timestamp_is_rejected():
    """非数字 timestamp 应被拒绝。"""
    signing_key = SigningKey.generate()
    platform = _make_platform(signing_key.verify_key.encode().hex())
    payload = {"type": 1}
    body = json.dumps(payload).encode("utf-8")

    message, response = platform.handle_webhook(
        _sign_headers(signing_key, body, timestamp="not-a-number"),
        body,
        payload,
    )

    assert message is None
    assert response is not None
    assert response.status_code == 401

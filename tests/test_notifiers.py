"""Unit tests for first-name resolution in tempo_certo.notifiers."""

import requests

from tempo_certo import config, notifiers


class _FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} error")

    def json(self):
        return self._json_data


def test_resolve_first_name_uses_config_and_skips_api(monkeypatch):
    monkeypatch.setattr(config, "USER_FIRST_NAME", "Stéfane")
    monkeypatch.setattr(config, "NOTIFY_METHOD", "telegram")

    def _boom(*args, **kwargs):
        raise AssertionError("the Telegram API must not be called when USER_FIRST_NAME is set")

    monkeypatch.setattr(notifiers.requests, "get", _boom)

    assert notifiers.resolve_first_name() == "Stéfane"


def test_resolve_first_name_falls_back_to_telegram_api(monkeypatch):
    monkeypatch.setattr(config, "USER_FIRST_NAME", "")
    monkeypatch.setattr(config, "NOTIFY_METHOD", "telegram")

    def _fake_get(url, params=None, timeout=None):
        return _FakeResponse({"ok": True, "result": {"first_name": "Léo"}})

    monkeypatch.setattr(notifiers.requests, "get", _fake_get)

    assert notifiers.resolve_first_name() == "Léo"


def test_resolve_first_name_none_when_api_fails(monkeypatch):
    monkeypatch.setattr(config, "USER_FIRST_NAME", "")
    monkeypatch.setattr(config, "NOTIFY_METHOD", "telegram")

    def _fake_get(url, params=None, timeout=None):
        raise requests.ConnectionError("network down")

    monkeypatch.setattr(notifiers.requests, "get", _fake_get)

    assert notifiers.resolve_first_name() is None


def test_resolve_first_name_none_when_not_telegram(monkeypatch):
    monkeypatch.setattr(config, "USER_FIRST_NAME", "")
    monkeypatch.setattr(config, "NOTIFY_METHOD", "ntfy")

    def _boom(*args, **kwargs):
        raise AssertionError("the Telegram API must not be called when NOTIFY_METHOD isn't telegram")

    monkeypatch.setattr(notifiers.requests, "get", _boom)

    assert notifiers.resolve_first_name() is None


def test_get_telegram_first_name_none_on_not_ok_response(monkeypatch):
    def _fake_get(url, params=None, timeout=None):
        return _FakeResponse({"ok": False})

    monkeypatch.setattr(notifiers.requests, "get", _fake_get)

    assert notifiers.get_telegram_first_name() is None


def test_get_telegram_first_name_none_on_missing_field(monkeypatch):
    def _fake_get(url, params=None, timeout=None):
        return _FakeResponse({"ok": True, "result": {}})

    monkeypatch.setattr(notifiers.requests, "get", _fake_get)

    assert notifiers.get_telegram_first_name() is None

"""Unit tests for the greeting built by tempo_certo.message_builder._accroche."""

from tempo_certo import config, message_builder
from tempo_certo.message_builder import _accroche


def test_accroche_with_first_name(monkeypatch):
    monkeypatch.setattr(config, "GREETING_ENABLED", True)
    monkeypatch.setattr(config, "LANGUAGE", "fr")
    monkeypatch.setattr(message_builder.i18n, "greeting_word", lambda: "Bonjour")

    accroche = _accroche("29/08/2026", "Stéfane")

    assert accroche == "Bonjour Stéfane, voici le récap météo d'aujourd'hui (29/08/2026) :"


def test_accroche_without_first_name(monkeypatch):
    monkeypatch.setattr(config, "GREETING_ENABLED", True)
    monkeypatch.setattr(config, "LANGUAGE", "fr")
    monkeypatch.setattr(message_builder.i18n, "greeting_word", lambda: "Bonjour")

    accroche = _accroche("29/08/2026", None)

    assert accroche == "Bonjour, voici le récap météo d'aujourd'hui (29/08/2026) :"

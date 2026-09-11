"""Testit turvalliselle malliratkaisulle."""

from __future__ import annotations

import pytest

from solution.secure_app import (
    MissingConfigurationError,
    get_api_key,
    hash_password,
    parse_age,
    public_error_message,
    validate_username,
    verify_password,
)

DEMO_ENV_KEY = "demo-test-key-not-real"
DEMO_PASSWORD = "Sininen-Kissa-2026"


def test_api_key_is_read_from_environment() -> None:
    environment = {"APP_API_KEY": DEMO_ENV_KEY}
    assert get_api_key(environment) == DEMO_ENV_KEY


def test_missing_api_key_raises_controlled_error() -> None:
    with pytest.raises(MissingConfigurationError):
        get_api_key({})


def test_empty_api_key_raises_controlled_error() -> None:
    with pytest.raises(MissingConfigurationError):
        get_api_key({"APP_API_KEY": "   "})


def test_valid_username_is_accepted() -> None:
    assert validate_username("matti") == "matti"
    assert validate_username("  Matti.2  ") == "Matti.2"


def test_finnish_unicode_username_is_accepted() -> None:
    assert validate_username("Sähkö-käyttäjä") == "Sähkö-käyttäjä"
    assert validate_username("Ääliö_123") == "Ääliö_123"


def test_empty_username_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_username("")
    with pytest.raises(ValueError):
        validate_username("   ")


def test_too_short_username_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_username("ab")


def test_too_long_username_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_username("a" * 31)


def test_username_with_forbidden_characters_is_rejected() -> None:
    with pytest.raises(ValueError):
        validate_username("user@name")
    with pytest.raises(ValueError):
        validate_username("matti kissa")
    with pytest.raises(ValueError):
        validate_username("admin!")


def test_valid_age_is_accepted() -> None:
    assert parse_age("0") == 0
    assert parse_age("18") == 18
    assert parse_age(120) == 120


def test_text_age_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_age("kahdeksantoista")


def test_negative_age_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_age(-1)


def test_age_over_120_is_rejected() -> None:
    with pytest.raises(ValueError):
        parse_age(121)


def test_password_hash_does_not_contain_plaintext() -> None:
    password_hash = hash_password(DEMO_PASSWORD)
    assert password_hash != DEMO_PASSWORD
    assert DEMO_PASSWORD not in password_hash


def test_correct_password_is_accepted() -> None:
    password_hash = hash_password(DEMO_PASSWORD)
    assert verify_password(DEMO_PASSWORD, password_hash) is True


def test_wrong_password_is_rejected() -> None:
    password_hash = hash_password(DEMO_PASSWORD)
    assert verify_password("Vaara-Salasana-999", password_hash) is False


def test_public_error_message_hides_exception_details() -> None:
    unique_text = "UNIIKKI-VIRHE-VIESTI-XYZ-987"
    error = RuntimeError(
        f"{unique_text} polku=C:\\Users\\demo\\salainen.txt"
    )
    message = public_error_message(error)

    assert isinstance(message, str)
    assert message.strip()
    assert unique_text not in message
    assert "salainen.txt" not in message
    assert "Users\\demo" not in message
    assert "Traceback" not in message
    assert "RuntimeError" not in message

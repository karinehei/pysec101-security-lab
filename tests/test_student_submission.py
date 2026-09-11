"""Testit opiskelijan palautukselle submission/app.py.

Jos palautustiedosto puuttuu, testit ohitetaan. Päähaaran CI ei suorita
tätä tiedostoa, joten puuttuva palautus ei riko julkista työnäytettä.
"""

from __future__ import annotations

import importlib.util
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_PATH = PROJECT_ROOT / "submission" / "app.py"

pytestmark = pytest.mark.skipif(
    not SUBMISSION_PATH.is_file(),
    reason=(
        "Opiskelijan palautus submission/app.py puuttuu. "
        "Kopioi exercise/insecure_app.py tiedostoksi submission/app.py "
        "ja aja testit uudelleen."
    ),
)

DEMO_ENV_KEY = "demo-test-key-not-real"
DEMO_PASSWORD = "Sininen-Kissa-2026"
REJECTION_ERRORS = (
    ValueError,
    TypeError,
    KeyError,
    LookupError,
    RuntimeError,
    OSError,
    AttributeError,
)


def assert_rejects(action: Callable[[], object]) -> None:
    """Varmista, että virheellinen syöte aiheuttaa hallitun virheen."""
    with pytest.raises(REJECTION_ERRORS):
        action()


@pytest.fixture
def app() -> ModuleType:
    spec = importlib.util.spec_from_file_location(
        "student_submission_app",
        SUBMISSION_PATH,
    )
    if spec is None or spec.loader is None:
        pytest.fail("submission/app.py:n lataaminen epäonnistui.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_api_key_is_read_from_environment(app: ModuleType) -> None:
    environment = {"APP_API_KEY": DEMO_ENV_KEY}
    assert app.get_api_key(environment) == DEMO_ENV_KEY


def test_missing_api_key_raises_controlled_error(app: ModuleType) -> None:
    assert_rejects(lambda: app.get_api_key({}))


def test_valid_username_is_accepted(app: ModuleType) -> None:
    assert app.validate_username("matti") == "matti"


def test_finnish_unicode_username_is_accepted(app: ModuleType) -> None:
    assert app.validate_username("Sähkö-käyttäjä") == "Sähkö-käyttäjä"


def test_empty_username_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.validate_username(""))


def test_too_short_username_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.validate_username("ab"))


def test_too_long_username_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.validate_username("a" * 31))


def test_username_with_forbidden_characters_is_rejected(
    app: ModuleType,
) -> None:
    assert_rejects(lambda: app.validate_username("user@name"))


def test_valid_age_is_accepted(app: ModuleType) -> None:
    assert app.parse_age("18") == 18


def test_text_age_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.parse_age("kahdeksantoista"))


def test_negative_age_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.parse_age(-1))


def test_age_over_120_is_rejected(app: ModuleType) -> None:
    assert_rejects(lambda: app.parse_age(121))


def test_password_hash_does_not_contain_plaintext(app: ModuleType) -> None:
    password_hash = app.hash_password(DEMO_PASSWORD)
    assert password_hash != DEMO_PASSWORD
    assert DEMO_PASSWORD not in password_hash


def test_correct_password_is_accepted(app: ModuleType) -> None:
    password_hash = app.hash_password(DEMO_PASSWORD)
    assert app.verify_password(DEMO_PASSWORD, password_hash) is True


def test_wrong_password_is_rejected(app: ModuleType) -> None:
    password_hash = app.hash_password(DEMO_PASSWORD)
    assert app.verify_password("Vaara-Salasana-999", password_hash) is False


def test_public_error_message_hides_exception_details(
    app: ModuleType,
) -> None:
    unique_text = "UNIIKKI-VIRHE-VIESTI-XYZ-987"
    error = RuntimeError(unique_text)
    message = app.public_error_message(error)

    assert isinstance(message, str)
    assert message.strip()
    assert unique_text not in message
    assert "RuntimeError" not in message

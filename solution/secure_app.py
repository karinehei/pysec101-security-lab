"""Turvallinen käyttäjän rekisteröintiesimerkki.

API-avain luetaan ympäristöstä, syöte validoidaan, salasana hajautetaan
Argon2-algoritmilla eikä käyttäjälle näytetä teknisiä virhetietoja.
"""

from __future__ import annotations

import unicodedata
from collections.abc import Mapping

from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, VerifyMismatchError

_PASSWORD_HASHER = PasswordHasher()
_ALLOWED_EXTRA_CHARS = {"_", "-", "."}
_GENERIC_PUBLIC_ERROR = (
    "Tapahtui odottamaton virhe. Yritä uudelleen myöhemmin."
)


class MissingConfigurationError(LookupError):
    """Pakollinen asetus puuttuu ympäristöstä."""


class ValidationError(ValueError):
    """Käyttäjän syöte ei täytä sääntöjä."""


def get_api_key(environment: Mapping[str, str]) -> str:
    """Palauta API-avain ympäristömuuttujasta APP_API_KEY.

    Args:
        environment: Ympäristömuuttujat, yleensä ``os.environ``.

    Raises:
        MissingConfigurationError: Jos ``APP_API_KEY`` puuttuu tai on tyhjä.
    """
    value = environment.get("APP_API_KEY")
    if value is None or not str(value).strip():
        raise MissingConfigurationError(
            "Pakollinen asetus APP_API_KEY puuttuu."
        )
    return str(value)


def _is_allowed_username_char(char: str) -> bool:
    """Palauta True, jos merkki on sallittu käyttäjänimessä."""
    if char in _ALLOWED_EXTRA_CHARS:
        return True
    category = unicodedata.category(char)
    return category.startswith(("L", "N"))


def validate_username(value: str) -> str:
    """Tarkista käyttäjänimi ja palauta siistitty arvo.

    Ympäröivät välilyönnit poistetaan. Pituuden pitää olla 3–30 merkkiä.
    Sallittuja merkkejä ovat Unicode-kirjaimet, numerot sekä ``_``, ``-``
    ja ``.``.
    """
    if not isinstance(value, str):
        raise ValidationError("Käyttäjänimen pitää olla merkkijono.")

    username = value.strip()
    if not 3 <= len(username) <= 30:
        raise ValidationError(
            "Käyttäjänimen pituuden pitää olla 3–30 merkkiä."
        )
    if not all(_is_allowed_username_char(char) for char in username):
        raise ValidationError("Käyttäjänimi sisältää kiellettyjä merkkejä.")
    return username


def parse_age(value: str | int) -> int:
    """Muunna ikä kokonaisluvuksi ja tarkista, että se on välillä 0–120."""
    if isinstance(value, bool) or value is None:
        raise ValidationError("Iän pitää olla kokonaisluku välillä 0–120.")

    try:
        age = int(value)
    except (TypeError, ValueError) as error:
        raise ValidationError(
            "Iän pitää olla kokonaisluku välillä 0–120."
        ) from error

    if isinstance(value, str) and str(value).strip() != str(age):
        raise ValidationError("Iän pitää olla kokonaisluku välillä 0–120.")

    if not 0 <= age <= 120:
        raise ValidationError("Iän pitää olla kokonaisluku välillä 0–120.")
    return age


def hash_password(password: str) -> str:
    """Palauta salasanan Argon2-tiiviste. Älä tallenna selväkielistä arvoa."""
    if not isinstance(password, str) or not password:
        raise ValidationError("Salasana ei saa olla tyhjä.")
    return _PASSWORD_HASHER.hash(password)


def verify_password(password: str, stored_value: str) -> bool:
    """Vertaa annettua salasanaa tallennettuun Argon2-tiivisteeseen."""
    try:
        return bool(_PASSWORD_HASHER.verify(stored_value, password))
    except (VerifyMismatchError, VerificationError, TypeError, ValueError):
        return False


def public_error_message(error: BaseException) -> str:
    """Palauta käyttäjälle turvallinen, yleinen virheilmoitus.

    Ilmoitus ei sisällä poikkeuksen tekstiä, tiedostopolkuja eikä kutsupinoa.
    """
    _ = error
    return _GENERIC_PUBLIC_ERROR


def register_user(
    username: str,
    age: str | int,
    password: str,
    environment: Mapping[str, str],
) -> dict[str, str | int]:
    """Rekisteröi käyttäjä validoitujen tietojen ja salasanatiivisteen kanssa."""
    get_api_key(environment)
    return {
        "username": validate_username(username),
        "age": parse_age(age),
        "password_hash": hash_password(password),
    }

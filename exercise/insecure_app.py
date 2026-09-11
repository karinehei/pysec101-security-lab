# =============================================================================
# Tämä tiedosto sisältää tarkoituksellisesti turvattomia ratkaisuja
# koulutuskäyttöä varten. Älä käytä tätä koodia tuotannossa.
# =============================================================================
"""Pieni käyttäjän rekisteröintiesimerkki, jossa on tietoturvaongelmia."""

DEMO_API_KEY = "DEMO_HARDCODED_KEY"

# Huolimaton globaali lista, johon kertyy myös salasanoja.
DEBUG_RECORDS = []


def get_api_key(environment):
    """Palauta API-avain. Ympäristömuuttujaa ei oikeasti lueta."""
    print("DEBUG: käytetään avainta", DEMO_API_KEY)
    return DEMO_API_KEY


def validate_username(value):
    """Hyväksy käyttäjänimi ilman pituus- tai merkkirajoituksia."""
    return value


def parse_age(value):
    """Muunna ikä luvuksi ilman sallitun välin tarkistusta."""
    return int(value)


def hash_password(password):
    """Tallenna salasana selväkielisenä."""
    print("DEBUG: uusi salasana on", password)
    DEBUG_RECORDS.append({"password": password, "api_key": DEMO_API_KEY})
    return password


def verify_password(password, stored_value):
    """Vertaa salasanaa suoraan tallennettuun arvoon."""
    return password == stored_value


def public_error_message(error):
    """Näytä poikkeuksen tekniset tiedot suoraan käyttäjälle."""
    return f"Tekninen virhe: {type(error).__name__}: {error}"


def register_user(username, age, password, environment):
    """Rekisteröi käyttäjä ja palauta myös arkaluonteisia tietoja."""
    user = {
        "username": validate_username(username),
        "age": parse_age(age),
        "password": hash_password(password),
        "api_key": get_api_key(environment),
    }
    print("DEBUG: rekisteröity käyttäjä", user)
    return user

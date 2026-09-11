# pysec101-security-lab

Koulutusprojekti Moodle-kurssille **Pythonin ja kyberturvallisuuden
perusteet**, harjoitukseen **Korjaa turvaton Python-ohjelma**.

Opiskelija saa pienen, tarkoituksellisesti turvattoman Python-ohjelman.
Tehtävänä on tunnistaa vähintään kolme tietoturvaongelmaa, korjata ne ja
osoittaa korjaukset pytest-testeillä.

## Varoitus

`exercise/insecure_app.py` sisältää tarkoituksellisesti turvattomia
ratkaisuja koulutuskäyttöä varten. Älä käytä tätä koodia tuotannossa.
Esimerkissä ei ole oikeita API-avaimia, tunnuksia, henkilötietoja,
`eval()`-kutsua eikä komentojen suorittamista.

Julkisessa työnäyteversiossa malliratkaisu on mukana arviointia varten.
Varsinaisessa koulutuksessa `solution`-kansio pidettäisiin opiskelijoilta
piilossa tai erillisessä opettajan repositoriossa.

## Oppimistavoitteet

Harjoituksen jälkeen opiskelija osaa:

- tunnistaa yleisiä tietoturvaongelmia pienestä Python-ohjelmasta
- siirtää salaisuudet pois lähdekoodista ympäristömuuttujiin
- validoida käyttäjän syötteen pituuden, merkit ja lukualueen
- hajauttaa salasanan valmiilla Argon2-toteutuksella
- näyttää käyttäjälle vain yleisen virheilmoituksen
- ajaa testit sekä Ruff-, Bandit- ja pip-audit-tarkistukset

## Hakemistorakenne

```text
pysec101-security-lab/
├── .github/
│   ├── workflows/
│   │   └── ci.yml
│   └── dependabot.yml
├── exercise/
│   ├── __init__.py
│   └── insecure_app.py
├── solution/
│   ├── __init__.py
│   └── secure_app.py
├── submission/
│   └── .gitkeep
├── tests/
│   ├── conftest.py
│   ├── test_solution.py
│   └── test_student_submission.py
├── .gitignore
├── LICENSE
├── README.md
├── SECURITY.md
├── requirements.txt
└── requirements-dev.txt
```

- `exercise/` — tarkoituksellisesti turvaton lähtökoodi
- `solution/` — turvallinen malliratkaisu
- `submission/` — opiskelijan oma korjattu tiedosto `app.py`
- `tests/` — malliratkaisun ja opiskelijapalautuksen testit
- `.github/` — GitHub Actions -CI ja Dependabot

## Asennus Windows PowerShellissa

1. Asenna [Python 3.12](https://www.python.org/downloads/) tai uudempi.
   Asennuksessa valitse *Add python.exe to PATH*.
2. Avaa PowerShell projektikansiossa.
3. Luo virtuaaliympäristö:

   ```powershell
   python -m venv .venv
   ```

4. Aktivoi virtuaaliympäristö:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Jos aktivointi estetään, suorita ensin:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```

5. Asenna riippuvuudet:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```

## Asennus Linuxissa ja macOS:ssa

1. Varmista, että Python 3.12 tai uudempi on asennettu:

   ```bash
   python3 --version
   ```

2. Luo virtuaaliympäristö:

   ```bash
   python3 -m venv .venv
   ```

3. Aktivoi virtuaaliympäristö:

   ```bash
   source .venv/bin/activate
   ```

4. Asenna riippuvuudet:

   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements-dev.txt
   ```

## Virtuaaliympäristön luominen

Virtuaaliympäristö erottaa kurssiprojektin kirjastot muista Python-projekteista.
Luo se projektin juureen komennolla `python -m venv .venv` (Windows) tai
`python3 -m venv .venv` (Linux ja macOS). Aktivoinnin jälkeen kehotteen
alussa näkyy `(.venv)`.

## Riippuvuuksien asentaminen

- `requirements.txt` sisältää ohjelman ajamiseen tarvittavan
  `argon2-cffi`-kirjaston.
- `requirements-dev.txt` sisältää lisäksi pytestin, Ruffin, Banditin ja
  pip-auditin.

Asenna kehitysriippuvuudet aktivoituun virtuaaliympäristöön:

```text
pip install -r requirements-dev.txt
```

## Harjoituksen suoritusohje

Tee vaiheet järjestyksessä:

1. Kloonaa tai lataa tämä repository.
2. Kopioi `exercise/insecure_app.py` tiedostoksi `submission/app.py`.

   Windows PowerShell:

   ```powershell
   Copy-Item exercise\insecure_app.py submission\app.py
   ```

   Linux ja macOS:

   ```bash
   cp exercise/insecure_app.py submission/app.py
   ```

3. Suorita opiskelijan testit (ne epäonnistuvat aluksi).
4. Tunnista vähintään kolme tietoturvaongelmaa turvattomasta ohjelmasta.
5. Korjaa `submission/app.py`. Älä muuta testitiedostoja.
6. Suorita testit uudelleen, kunnes ne läpäisevät.
7. Palauta Moodleen korjattu tiedosto, perustelut ja testitulokset tai
   kuvakaappaus.

Turvallisen malliratkaisun julkinen rajapinta, joka sinun tulee toteuttaa:

- `get_api_key(environment)`
- `validate_username(value)`
- `parse_age(value)`
- `hash_password(password)`
- `verify_password(password, stored_value)`
- `public_error_message(error)`

Korjauksissa:

- Lue API-avain ympäristömuuttujasta `APP_API_KEY`.
- Hylkää puuttuva asetus hallitulla virheellä.
- Siisti ja validoi käyttäjänimi (3–30 merkkiä; Unicode-kirjaimet, numerot,
  `_`, `-` ja `.`).
- Hyväksy ikä vain kokonaislukuna välillä 0–120.
- Hajauta salasana `argon2-cffi`-kirjaston `PasswordHasher`-luokalla.
- Näytä käyttäjälle vain yleinen virheilmoitus.

Älä toteuta omaa salaus- tai hajautusalgoritmia. Älä tulosta salasanoja tai
API-avaimia. Nosta virheellisestä syötteestä ja puuttuvasta asetuksesta
hallittu poikkeus, esimerkiksi `ValueError` tai `LookupError`.

## Testien suorittaminen

Opiskelijan palautuksen testit:

```text
pytest tests/test_student_submission.py -v
```

Jos `submission/app.py` puuttuu, testit ohitetaan selkeällä ilmoituksella.
Kun kopioit turvattoman tiedoston submission-kansioon, testien pitää
epäonnistua. Korjauksen jälkeen samojen testien pitää läpäistä.

Malliratkaisun testit (opettajan tai työnäytteen tarkistus):

```text
pytest tests/test_solution.py -v
```

Päähaaran CI ajaa vain malliratkaisun testit. Puuttuva opiskelijapalautus ei
siis riko julkista repositorya.

## Tietoturvatarkistusten suorittaminen

```text
ruff check solution tests
bandit -r solution
pip-audit -r requirements.txt
```

Banditia ei ajeta `exercise`-kansiolle, koska se sisältää tarkoituksellisesti
turvattoman koulutusesimerkin.

## Palautusohje Moodleen

Palauta Moodle-tehtävään:

1. Korjattu tiedosto `submission/app.py`.
2. Lyhyt perustelu, jossa nimeät vähintään kolme tunnistamaasi
   tietoturvaongelmaa ja kerrot, miten korjasit ne.
3. Testitulos tai kuvakaappaus komennosta
   `pytest tests/test_student_submission.py -v`.

Älä palauta virtuaaliympäristöä, salaisuuksia tai `.env`-tiedostoa.

## Arviointimatriisi

| Osio | Pisteet |
| --- | --- |
| Riskien tunnistaminen | 0–2 |
| Korjausten turvallisuus | 0–2 |
| Ohjelman toimivuus ja testit | 0–2 |
| Muutosten perustelut | 0–2 |
| **Hyväksymisraja** | **6/8** |

## Lähteet

- OWASP Secure Product Design Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Secure_Product_Design_Cheat_Sheet.html
- OWASP Secrets Management Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
- OWASP Input Validation Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
- OWASP Password Storage Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
- OWASP Error Handling Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html
- OWASP Vulnerable Dependency Management Cheat Sheet:
  https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html
- Python `os.getenv()`:
  https://docs.python.org/3/library/os.html#os.getenv
- PyPA pip-audit:
  https://github.com/pypa/pip-audit

## Tekoälyn käyttö

Projektin rakenteen, tekstien ja koodiesimerkkien luonnostelussa on
hyödynnetty generatiivista tekoälyä. Sisältö on tarkistettu, testattu ja
muokattu projektin oppimistavoitteiden mukaiseksi. Tekoälyä ei ole käytetty
itsenäisenä tietolähteenä.

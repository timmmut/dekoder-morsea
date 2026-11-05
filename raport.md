# [KM] Koder i dekoder alfabetu Morse'a

## Spis treści

1. [About](#about)
2. [Technologies](#technologies)
3. [Project structure](#project-structure)
4. [Getting started](#getting-started)
5. [Usage](#usage)
6. [Administration](#administration)
7. [Contacts](#contacts)

## About

Projekt umożliwia kodowanie tekstu alfabetem Morse'a, zapis wiadomości do XML oraz jej odczyt i dekodowanie. Koder grupy A i dekoder grupy B sprawdzają XML względem wspólnego schematu XSD, odpowiednio przed pobraniem pliku i przed jego dekodowaniem. Oba interfejsy działają w przeglądarce.

## Technologies

- Python 3.12 w obrazie Docker; lokalnie projekt wymaga Pythona 3.10 lub nowszego.
- `lxml` 5.x–6.x — obsługa XML i walidacja XSD.
- Streamlit 1.40–1.x — interfejs kodera.
- Flask 3.x i Waitress 3.x — interfejs i serwer dekodera.
- Docker i Docker Compose — uruchamianie usług.

Zakresy zależności znajdują się w `requirements.txt`. Nie dodano zależności wymagających płatnej licencji; szczegóły licencji poszczególnych bibliotek znajdują się w ich dokumentacji.

## Project structure

```text
/
├── koder.py              # koder i interfejs Streamlit
├── dekoder.py            # walidacja XML i dekodowanie
├── web.py                # przeglądarkowy interfejs dekodera
├── main.py               # alternatywny interfejs Tkinter dekodera
├── templates/index.html  # szablon dekodera
├── morse.xsd             # wspólny schemat XML
├── przyklad.xml          # przykładowa wiadomość
├── tests/                # testy jednostkowe i integracyjne
├── Dockerfile            # obraz aplikacji
├── compose.yaml          # konfiguracja obu usług
├── requirements.txt      # zależności Pythona
├── README.md             # instrukcja użytkowania
└── raport.md             # ten raport
```

## Getting started

### Prerequisites

Docker Desktop na Windows/macOS lub Docker Engine z wtyczką Compose na Linuksie oraz przeglądarka. Porty lokalne 8000 i 8501 powinny być wolne.

### Development environment setup

Pobierz repozytorium jako ZIP i rozpakuj je albo sklonuj przez Git. Do lokalnego uruchamiania bez Dockera potrzebne są Python 3.10+ i zależności z `requirements.txt`.

### Installation

Uruchom Docker, otwórz terminal w katalogu projektu i wykonaj:

```sh
docker compose up --build
```

Koder jest dostępny pod `http://localhost:8501`, a dekoder pod `http://localhost:8000`. Pierwsze uruchomienie pobiera obraz i instaluje zależności. Weryfikacja budowania obrazu Docker pozostaje do wykonania na komputerze z uruchomionym Dockerem.

### Sanity test

W koderze wpisz `SOS TEST`, wygeneruj i pobierz XML. Wybierz plik w dekoderze: wynik powinien wynosić `SOS TEST`. Niepoprawny XML powinien zostać odrzucony. Lokalne testy Pythona, po instalacji zależności, uruchamia `python -m unittest discover -s tests`.

## Usage

1. Grupa A podaje nadawcę i tekst, a następnie generuje zwalidowany plik XML.
2. Grupa B wybiera otrzymany XML w dekoderze. Aplikacja weryfikuje go względem `morse.xsd`, po czym wyświetla kod i wynik.

Koder obsługuje litery A–Z, ĄĆĘŁŃÓŚŹŻ oraz cyfry; pozostałe znaki pomija. Dekoder obsługuje również określone znaki interpunkcyjne. W pliku XML litery oddzielają spacje, a słowa — `/` otoczony spacjami.

## Administration

Zatrzymaj aplikację przez `Ctrl+C`, usuń kontenery poleceniem `docker compose down`, a po zmianach uruchom ponownie przez `docker compose up --build`. Zmień port hosta w `compose.yaml`, jeśli jest zajęty. Usługi są domyślnie dostępne tylko lokalnie; nie ma kont użytkowników ani domyślnych haseł. Aplikacja nie przechowuje wiadomości trwale; kopie plików XML należy zachować osobno, jeśli są potrzebne.

## Contacts

- Grupa A — koder: **do uzupełnienia przez zespół**.
- Grupa B — dekoder: **do uzupełnienia przez zespół**.
- Członkowie repozytorium: [timmmut](https://github.com/timmmut), [Boguszera](https://github.com/Boguszera), [Slugmyy](https://github.com/Slugmyy), [mdobierski](https://github.com/mdobierski) — role i dane kontaktowe do potwierdzenia.
- Prowadzący: kontakt zgodnie z instrukcją projektu — `rafal.renk@gmail.com`.
# Koder i dekoder alfabetu Morse'a

Koder grupy A generuje i waliduje plik XML, a dekoder grupy B sprawdza go względem schematu XSD i wyświetla odkodowany tekst.

## Uruchomienie w Dockerze — Windows, macOS i Linux

Zainstaluj i uruchom Docker Desktop (Windows/macOS) albo Docker Engine z wtyczką Compose (Linux). Pobierz projekt z GitHub przez **Code → Download ZIP** i rozpakuj go lub sklonuj repozytorium. W terminalu w folderze projektu uruchom:

```sh
docker compose up --build
```

Otwórz **http://localhost:8501** (koder) i **http://localhost:8000** (dekoder). W koderze wpisz tekst i pobierz zweryfikowany plik XML; w dekoderze wybierz ten plik, by ponownie go zweryfikować i odkodować. Możesz też użyć `przyklad.xml`. Pierwsze uruchomienie pobierze obraz Pythona i zależności. Zatrzymaj aplikację przez `Ctrl+C`; kontenery można usunąć poleceniem `docker compose down`. Jeśli port jest zajęty, zmień port po lewej stronie odpowiedniego mapowania w `compose.yaml`, np. `127.0.0.1:8001:8000`, i użyj go w adresie przeglądarki.

Wersja dockerowa działa przez przeglądarkę; Docker i przeglądarka wystarczą, nie trzeba instalować Pythona ani konfigurować Gita. Pliki XML są przesyłane lokalnie do aplikacji, przechowywane tymczasowo i usuwane po przetworzeniu. Maksymalny rozmiar żądania wynosi 1 MB. Usługa jest domyślnie dostępna tylko na komputerze, na którym ją uruchomiono.

## Uruchomienie bez Dockera (Windows)

Potrzebny jest Python 3.10 lub nowszy z modułem Tkinter. W katalogu projektu:

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python main.py
```

W aplikacji wybierz plik `przyklad.xml` i kliknij „Sprawdź XML i dekoduj”. Testy: `.\.venv\Scripts\python -m unittest discover -s tests`.

## Format wymiany

Schemat znajduje się w `morse.xsd`, a przykładowa wiadomość w `przyklad.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<morseMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
							xsi:noNamespaceSchemaLocation="morse.xsd">
	<sender>Grupa A</sender>
	<timestamp>2026-11-05T13:30:00</timestamp>
	<content>... --- ... / - . ... -</content>
</morseMessage>
```

Elementy są wymagane w kolejności: `sender` (nadawca), `timestamp` (data i czas w formacie `xs:dateTime`) oraz `content` (kod Morse'a). W kodzie kropka i minus oznaczają sygnały, spacje oddzielają litery, a samodzielny `/` oddziela słowa. Przykład oznacza `SOS TEST`. Sam znak ukośnika w tekście koduje się jako `-..-.`. Schemat dopuszcza w `content` wyłącznie kropki, minusy, ukośniki i zwykłe spacje.

Koder obsługuje litery A–Z, polskie litery ĄĆĘŁŃÓŚŹŻ i cyfry. Inne znaki, w tym interpunkcję, pomija. Dekoder obsługuje te litery i cyfry oraz typowe znaki interpunkcyjne wymienione w `dekoder.py`; wynik jest zapisywany wielkimi literami. Nieznane kody i niepoprawne separatory są zgłaszane jako błędy. XML z DTD jest odrzucany.

Dekoder korzysta z lokalnego pliku `morse.xsd`, niezależnie od lokalizacji schematu podanej w XML. Przykładowy plik nie zastępuje pliku przygotowanego przez zespół kodujący.
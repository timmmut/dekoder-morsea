# Dekoder alfabetu Morse'a

Aplikacja zespołu dekodującego: odczytuje plik XML, sprawdza jego zgodność z lokalnym schematem XSD i wyświetla tekst po dekodowaniu.

## Uruchomienie

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

Obsługiwane są litery A–Z, cyfry i typowe znaki interpunkcyjne wymienione w `dekoder.py`; wynik jest zapisywany wielkimi literami. Polskie litery nie są obecnie obsługiwane. Nieznane kody i niepoprawne separatory są zgłaszane jako błędy. XML z DTD jest odrzucany.

Dekoder korzysta z lokalnego pliku `morse.xsd`, niezależnie od lokalizacji schematu podanej w XML. Przykładowy plik nie zastępuje pliku przygotowanego przez zespół kodujący.
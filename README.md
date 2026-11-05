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

## Proponowany format wymiany

**Ten format trzeba uzgodnić z zespołem kodującym**; nie zakładamy, że został narzucony w zadaniu. Schemat znajduje się w `wiadomosc.xsd`, a przykładowa wiadomość w `przyklad.xml`. XML zawiera jeden element `<wiadomosc>` z kodem Morse'a: kropka i minus oznaczają sygnały, białe znaki oddzielają litery, a samodzielny `/` oddziela słowa. Na przykład `... --- ... / .-` oznacza `SOS A`. Sam znak ukośnika w tekście koduje się jako `-..-.`.

Obsługiwane są litery A–Z, cyfry i typowe znaki interpunkcyjne wymienione w `dekoder.py`; wynik jest zapisywany wielkimi literami. Polskie litery nie są obecnie obsługiwane. Nieznane kody i niepoprawne separatory są zgłaszane jako błędy. XML z DTD jest odrzucany.

Zmiany w uzgodnionym formacie wymagają dostosowania schematu, dekodera i testów. Przykładowy plik nie zastępuje pliku przygotowanego przez zespół kodujący.
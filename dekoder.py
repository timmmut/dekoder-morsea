"""Dekoder wiadomości Morse'a zapisanej w pliku XML."""

from pathlib import Path
import re

from lxml import etree


SCHEMAT = Path(__file__).with_name("morse.xsd")

KODY = {
    ".-": "A", "-...": "B", "-.-.": "C", "-..": "D", ".": "E",
    "..-.": "F", "--.": "G", "....": "H", "..": "I", ".---": "J",
    "-.-": "K", ".-..": "L", "--": "M", "-.": "N", "---": "O",
    ".--.": "P", "--.-": "Q", ".-.": "R", "...": "S", "-": "T",
    "..-": "U", "...-": "V", ".--": "W", "-..-": "X", "-.--": "Y",
    "--..": "Z", "-----": "0", ".----": "1", "..---": "2",
    "...--": "3", "....-": "4", ".....": "5", "-....": "6",
    "--...": "7", "---..": "8", "----.": "9", ".-.-.-": ".",
    "--..--": ",", "..--..": "?", ".----.": "'", "-.-.--": "!",
    "-..-.": "/", "-.--.": "(", "-.--.-": ")", ".-...": "&",
    "---...": ":", "-.-.-.": ";", "-...-": "=", ".-.-.": "+",
    "-....-": "-", "..--.-": "_", ".-..-.": '"', "...-..-": "$",
    ".--.-.": "@", ".-..-": "Ł", "..-..": "Ę",
}


def dekoduj_morse(kod: str) -> str:
    """Litery oddziela spacja, a słowa znak / otoczony spacjami."""
    kod = kod.strip()
    if not kod:
        raise ValueError("Wiadomość jest pusta.")
    tokeny = kod.split()
    slowa = []
    aktualne = []
    for token in tokeny:
        if token == "/":
            if not aktualne:
                raise ValueError("Nieprawidłowy separator słów '/'.")
            slowa.append("".join(aktualne))
            aktualne = []
        elif not re.fullmatch(r"[.-]+", token):
            raise ValueError(f"Nieprawidłowy zapis kodu: {token!r}.")
        elif token not in KODY:
            raise ValueError(f"Nieznany znak Morse'a: {token}.")
        else:
            aktualne.append(KODY[token])
    if not aktualne:
        raise ValueError("Wiadomość nie może kończyć się separatorem słów.")
    slowa.append("".join(aktualne))
    return " ".join(slowa)


def odczytaj_xml(sciezka: str | Path) -> tuple[str, str]:
    """Waliduje XML względem lokalnego XSD, a następnie dekoduje wiadomość."""
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    try:
        schemat = etree.XMLSchema(etree.parse(str(SCHEMAT), parser))
        dokument = etree.parse(str(sciezka), parser)
        if dokument.docinfo.doctype:
            raise ValueError("Deklaracje DTD nie są obsługiwane.")
        schemat.assertValid(dokument)
    except (OSError, etree.LxmlError) as blad:
        raise ValueError(f"Nie udało się odczytać lub zweryfikować XML: {blad}") from blad
    kod = dokument.getroot().findtext("content") or ""
    return kod.strip(), dekoduj_morse(kod)
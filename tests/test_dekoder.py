import tempfile
import unittest
from pathlib import Path

from dekoder import dekoduj_morse, odczytaj_xml


class TestDekoder(unittest.TestCase):
    def test_tekst_i_interpunkcja(self):
        self.assertEqual(dekoduj_morse("... --- ... / .---- ..--.."), "SOS 1?")
        self.assertEqual(dekoduj_morse("-..-."), "/")

    def test_wiadomosc_z_litera_l(self):
        xml = ('<?xml version="1.0" encoding="UTF-8"?>'
               '<morseMessage xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
               'xsi:noNamespaceSchemaLocation="morse.xsd">'
               '<sender>paweł</sender><timestamp>2026-11-05T14:02:33</timestamp>'
               '<content>.--. .- .-- . .-..- / -- .- / -. .- / .. -- .. ..-.. / '
               '.--. .- .-- . .-..-</content></morseMessage>')
        with tempfile.TemporaryDirectory() as folder:
            plik = Path(folder) / "message.xml"
            plik.write_text(xml, encoding="utf-8")
            _, wynik = odczytaj_xml(plik)
        self.assertEqual(wynik, "PAWEŁ MA NA IMIĘ PAWEŁ")

    def test_bledny_kod(self):
        for kod in ("", "... /", "/ ...", "... / / ---", ".../...", "........"):
            with self.subTest(kod=kod), self.assertRaises(ValueError):
                dekoduj_morse(kod)

    def test_przyklad(self):
        kod, tekst = odczytaj_xml(Path(__file__).resolve().parents[1] / "przyklad.xml")
        self.assertEqual(tekst, "SOS TEST")
        self.assertTrue(kod.startswith("..."))

    def test_nieprawidlowy_xml(self):
        przypadki = (
            "<inne>...</inne>",
            "<wiadomosc>...</wiadomosc>",
            "<morseMessage><sender>Grupa A</sender><timestamp>zła data</timestamp><content>...</content></morseMessage>",
            "<morseMessage><sender>Grupa A</sender><timestamp>2026-11-05T13:30:00</timestamp><content>abc</content></morseMessage>",
            "<morseMessage><sender>Grupa A</sender><timestamp>2026-11-05T13:30:00</timestamp><content/></morseMessage>",
            "<morseMessage><timestamp>2026-11-05T13:30:00</timestamp><content>...</content></morseMessage>",
            "<morseMessage><timestamp>2026-11-05T13:30:00</timestamp><sender>Grupa A</sender><content>...</content></morseMessage>",
            "<!DOCTYPE morseMessage><morseMessage><sender>A</sender><timestamp>2026-11-05T13:30:00</timestamp><content>...</content></morseMessage>",
        )
        for zawartosc in przypadki:
            with self.subTest(zawartosc=zawartosc), tempfile.TemporaryDirectory() as folder:
                plik = Path(folder) / "test.xml"
                plik.write_text(zawartosc, encoding="utf-8")
                with self.assertRaises(ValueError):
                    odczytaj_xml(plik)


if __name__ == "__main__":
    unittest.main()
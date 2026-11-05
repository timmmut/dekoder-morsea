import tempfile
import unittest
from pathlib import Path

from dekoder import odczytaj_xml
from koder import encode_to_morse, generate_and_validate_xml


class TestIntegracja(unittest.TestCase):
    def test_wszystkie_znaki_kodera(self):
        tekst = "ABCDEFGHIJKLMNOPQRSTUVWXYZ ĄĆĘŁŃÓŚŹŻ 0123456789"
        kod, _ = encode_to_morse(tekst)
        xml = generate_and_validate_xml("Grupa A", kod)
        with tempfile.TemporaryDirectory() as folder:
            plik = Path(folder) / "wiadomosc.xml"
            plik.write_bytes(xml)
            kod_odczytany, wynik = odczytaj_xml(plik)
        self.assertEqual(kod_odczytany, kod)
        self.assertEqual(wynik, tekst)

    def test_koder_pomija_nieobslugiwane_znaki(self):
        kod, _ = encode_to_morse("A, B!")
        self.assertEqual(kod, ".- / -...")


if __name__ == "__main__":
    unittest.main()
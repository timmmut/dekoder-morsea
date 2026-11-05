import io
import unittest
from pathlib import Path

from web import app


class TestInterfejsWebowy(unittest.TestCase):
    def setUp(self):
        self.klient = app.test_client()

    def test_strona(self):
        odpowiedz = self.klient.get("/")
        self.assertEqual(odpowiedz.status_code, 200)
        self.assertIn("Dekoder wiadomości", odpowiedz.get_data(as_text=True))

    def test_poprawny_xml(self):
        plik = Path(__file__).resolve().parents[1] / "przyklad.xml"
        with plik.open("rb") as dane:
            odpowiedz = self.klient.post("/", data={"plik": (dane, "przyklad.xml")})
        self.assertEqual(odpowiedz.status_code, 200)
        self.assertIn("SOS TEST", odpowiedz.get_data(as_text=True))

    def test_bledne_dane(self):
        for dane in ({}, {"plik": (io.BytesIO(b"abc"), "plik.txt")},
                     {"plik": (io.BytesIO(b"<inne/>"), "plik.xml")}):
            with self.subTest(dane=dane):
                self.assertEqual(self.klient.post("/", data=dane).status_code, 400)

    def test_limit_rozmiaru(self):
        odpowiedz = self.klient.post("/", data={"plik": (io.BytesIO(b"x" * (1024 * 1024 + 1)), "plik.xml")})
        self.assertEqual(odpowiedz.status_code, 413)


if __name__ == "__main__":
    unittest.main()
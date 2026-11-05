"""Przeglądarkowy interfejs dekodera wiadomości XML."""

from pathlib import Path
from tempfile import TemporaryDirectory

from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from dekoder import odczytaj_xml


app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024


@app.errorhandler(RequestEntityTooLarge)
def zbyt_duzy_plik(_blad):
    return render_template("index.html", blad="Plik jest za duży. Maksymalny rozmiar żądania to 1 MB."), 413


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")

    plik = request.files.get("plik")
    if not plik or not plik.filename:
        return render_template("index.html", blad="Wybierz plik XML."), 400
    if not plik.filename.lower().endswith(".xml"):
        return render_template("index.html", blad="Wybierz plik z rozszerzeniem .xml."), 400

    try:
        with TemporaryDirectory() as folder:
            sciezka = Path(folder) / "wiadomosc.xml"
            plik.save(sciezka)
            kod, wynik = odczytaj_xml(sciezka)
    except ValueError as blad:
        return render_template("index.html", blad=f"Niepoprawny plik lub kod Morse'a: {blad}"), 400

    return render_template("index.html", kod=kod, wynik=wynik)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8000)
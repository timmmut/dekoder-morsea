"""Okno aplikacji dekodującej alfabet Morse'a."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from dekoder import odczytaj_xml


def main() -> None:
    okno = tk.Tk()
    okno.title("Dekoder alfabetu Morse'a")
    okno.geometry("700x450")
    okno.minsize(480, 360)

    ramka = ttk.Frame(okno, padding=18)
    ramka.pack(fill="both", expand=True)
    ttk.Label(ramka, text="Dekoder alfabetu Morse'a", font=("Segoe UI", 18, "bold")).pack(anchor="w")
    ttk.Label(ramka, text="Wybierz plik XML. Przed dekodowaniem zostanie sprawdzony schemat XSD.", wraplength=620).pack(anchor="w", pady=(4, 14))
    sciezka = tk.StringVar()
    wiersz = ttk.Frame(ramka)
    wiersz.pack(fill="x")
    ttk.Entry(wiersz, textvariable=sciezka).pack(side="left", fill="x", expand=True)

    def wybierz() -> None:
        plik = filedialog.askopenfilename(title="Wybierz wiadomość", filetypes=[("Pliki XML", "*.xml"), ("Wszystkie pliki", "*.*")])
        if plik:
            sciezka.set(plik)

    ttk.Button(wiersz, text="Wybierz plik", command=wybierz).pack(side="left", padx=(8, 0))
    ttk.Label(ramka, text="Kod Morse'a").pack(anchor="w", pady=(14, 2))
    kod_pole = tk.Text(ramka, height=4, wrap="word")
    kod_pole.pack(fill="both", expand=True)
    ttk.Label(ramka, text="Odkodowany tekst").pack(anchor="w", pady=(10, 2))
    wynik_pole = tk.Text(ramka, height=4, wrap="word")
    wynik_pole.pack(fill="both", expand=True)

    def dekoduj() -> None:
        for pole in (kod_pole, wynik_pole):
            pole.delete("1.0", "end")
        if not sciezka.get().strip():
            messagebox.showwarning("Brak pliku", "Wybierz plik XML.")
            return
        try:
            kod, wynik = odczytaj_xml(sciezka.get().strip())
        except ValueError as blad:
            messagebox.showerror("Błąd dekodowania", str(blad))
            return
        kod_pole.insert("1.0", kod)
        wynik_pole.insert("1.0", wynik)

    ttk.Button(ramka, text="Sprawdź XML i dekoduj", command=dekoduj).pack(anchor="e", pady=(12, 0))
    okno.mainloop()


if __name__ == "__main__":
    main()
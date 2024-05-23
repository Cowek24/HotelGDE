from datetime import datetime

# Szoba osztály definiálása, melynek két fő tulajdonsága (attribútuma) van: A száma, és az ára
class Szoba:
    def __init__(self, ar, szobaszam):
        self.ar = ar
        self.szobaszam = szobaszam
    def info(self):
        return f"Szoba - szobaszam: {self.szobaszam}, Ár: {self.ar} Ft"
# Egyágyas szobák - első emelet
class EgyagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=24000, szobaszam=szobaszam)
    def info(self):
        return f"Egyágyas szoba - szobaszam: {self.szobaszam}, Ár: {self.ar} Ft"
# Kétágyas szoba - második emeleten}
class KetagyasSzoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=32000, szobaszam=szobaszam)
    def info(self):
        return f"Kétágyas szoba - szobaszam: {self.szobaszam}, Ár: {self.ar} Ft"
class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []
# itt adjuk hozzá a szobát a szobák listájához
    def szoba_hozzaadasa(self, szoba):
        self.szobak.append(szoba)
    def szobak_listazasa(self):
        for szoba in self.szobak:
            print(szoba.info())
    # Ellenőrzés, hogy van-e már foglalás erre a szobára és dátumra
    def foglalas(self, szobaszam, datum, vendeg_neve):
        try:
            foglalas_datum = datetime.strptime(datum, "%Y.%m.%d")
            if foglalas_datum <= datetime.now():
                print("A dátum érvénytelen. Csak jövőbeli dátumokra lehet foglalni.")
                return None
        except ValueError:
            print("A dátum formátuma érvénytelen. Kérjük, használja a következő formátumot: ÉÉÉÉ.HH.NN")
            return None
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                print("Ez a szoba már foglalt ezen a napon.")
                return None

# ez a foglalási metódus - ha valami nem stimmel, nem foglalja le (pl: szobaszam nem létezik)
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                uj_foglalas = Foglalas(szoba, datum, vendeg_neve)
                self.foglalasok.append(uj_foglalas)
                return uj_foglalas.szoba.ar
        return None

# a lemondás gyakorlatilag egy fordított foglalás
    def foglalas_lemondasa(self, szobaszam, datum):
        for foglalas in self.foglalasok:
            if foglalas.szoba.szobaszam == szobaszam and foglalas.datum == datum:
                self.foglalasok.remove(foglalas)
                return True
        return False

# nézzük csak meg mit tároltunk el...
    def foglalasok_listazasa(self):
        for foglalas in self.foglalasok:
            print(foglalas.info())
class Foglalas:
    def __init__(self, szoba, datum, vendeg_neve):
        self.szoba = szoba
        self.datum = datum
        self.vendeg_neve = vendeg_neve

    def info(self):
        return f"Foglalás - Vendég neve: {self.vendeg_neve}, Szoba: {self.szoba.info()}, datum: {self.datum}"


# itt hozzuk létre a hotelünket - kedvünkre bővíthetjük a szobák számát
def main():
    szalloda = Szalloda("GDE OOP Hotel")
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(101))
    szalloda.szoba_hozzaadasa(EgyagyasSzoba(102))
    szalloda.szoba_hozzaadasa(KetagyasSzoba(103))

    elozetes_foglalasok = [
            (101, "2024.06.01", "Teszt Vendég1"),
            (102, "2024.06.02", "Teszt Vendég2"),
            (103, "2024.06.03", "Teszt Vendég3"),
            (101, "2024.06.04", "Teszt Vendég4"),
            (102, "2024.06.05", "Teszt Vendég5")
    ]
    for szobaszam, datum, vendeg_neve in elozetes_foglalasok:
            szalloda.foglalas(szobaszam, datum, vendeg_neve)

# a menü szerkezete:
    while True:
        print("1. Szobák listázása")
        print("2. Szoba foglalása")
        print("3. Foglalás lemondása")
        print("4. Foglalások listázása")
        print("5. Kilépés")
        valasztas = input("Válassz egy opciót: ")

# a menüpontoknak megfelelő működés - jó sok feltételes elágazással fűszerezve:

        if valasztas == '1':
            szalloda.szobak_listazasa()
        elif valasztas == '2':
            szobaszam = int(input("Add meg a szobaszamot: "))
            datum = input("Add meg a datumot (ÉÉÉÉ.HH.NN): ")
            vendeg_neve = input("Add meg a vendég nevét: ")
            ar = szalloda.foglalas(szobaszam, datum, vendeg_neve)
            if ar:
                print(f"Foglalás sikeres, ár: {ar} Ft")
            else:
                print("Nem sikerült a foglalás.")
        elif valasztas == '3':
            szobaszam = int(input("Add meg a szobaszámot: "))
            datum = input("Add meg a datumot (ÉÉÉÉ.HH.NN): ")
            sikeres = szalloda.foglalas_lemondasa(szobaszam, datum)
            if sikeres:
                print("Foglalás lemondva.")
            else:
                print("Nem sikerült lemondani a foglalást.")
        elif valasztas == '4':
            szalloda.foglalasok_listazasa()
        elif valasztas == '5':
            break
        else:
            print("Érvénytelen választás.")

if __name__ == "__main__":
    main()

# az igazi az lett volna ha TXT-be kírja folyamatosan a foglalásokat, majd indításnál mindig visszaolvassa azt.
# Persze akkor az elmúlt dátumok okoznak problémát, azt is le kellett volna kezelni. Lett volna hozzá kedvem, de időm most nem :-/
# Elengedtem mert nem volt a feladat része, csak jól esett volna :-)

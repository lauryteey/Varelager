import json
import os 

FILENAME = "varer.json"

#Funksjoner for å lagre og skrive data fra JSON filen 

def last_data():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, "r", encoding="utf-8") as f:
        return json.load(f)
    
def write_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        return json.dump(data, f, indent= 4)
    
#Funksjon for å clear terminalen etter å bruke en funksjon 
def clearScreen():
    os.system("cls" if os.name == "nt" else "clear")

    
#Funksjon for å printe menyen og funksjoner til menyen 

def printMeny():
    clearScreen()
    print("------------------- Din varerlager -------------------")
    print("| 1. Registrer nye varer                              |")
    print("| 2. Vise antall varer på din lager                   |")
    print("| 3. søke etter varer                                 |")
    print("| 4. Vis en kategori                                  |")
    print("| 5. Oppdater antall varer ved inn -og utlevering     |")
    print("| 6. Rapport over lagerstatus                         |")
    print("| 7. Slett en vare                                    |")
    print("| 8. Slutt                                            |")
    print("------------------------------------------------------")
    menyvalg = input("Vennligst skriv inn tall for å velge fra menyen: ")
    utfoerMenyvalg(menyvalg)
    
def utfoerMenyvalg(valgtTall):
    if valgtTall == "1":
        registrerVarer()
    elif valgtTall == "2":
        antallVarer()
        printMeny()
    elif valgtTall == "3":
        søkVarer() 
    elif valgtTall == "4":
        visKategori()
    elif valgtTall == "5":
        OppdaterVarer()
    elif valgtTall == "6":
        lagerStatus()
    elif valgtTall == "7":
        slettVare()
    elif valgtTall == "8":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if (bekreftelse == "J" or bekreftelse == "j" or bekreftelse == "ja"):
            exit()
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-6: ")
        utfoerMenyvalg(nyttForsoek)
        
        
#Funksjoner fra menyen 

def registrerVarer(): 
    data = last_data()

    # Navn med maks 20 tegn, bare bokstaver og mellomrom
    while True:
        navn = input("Navn på varen (maks 20 tegn): ").strip()
        if len(navn) == 0 or len(navn) > 20 or not navn.replace(" ", "").isalpha():
            print(" Ugyldig navn. Bruk bare bokstaver og maks 20 tegn.")
        else:
            break

    # Kategori med maks 15 tegn
    while True:
        kategori = input("Kategori (f.eks. Elektronikk): ").strip()
        if len(kategori) == 0 or len(kategori) > 15:
            print(" Kategori må være mellom 1 og 15 tegn.")
        else:
            break

    # Antall: bare heltall mellom 0 og 10000
    while True:
        try:
            antall = int(input("Antall på lager (0–10000): "))
            if 0 <= antall <= 10000:
                break
            else:
                print("Antall må være mellom 0 og 10000.")
        except ValueError:
            print(" Du må skrive et helt tall.")

    # Pris: kun positivt tall, maks 99999.99
    while True:
        try:
            pris = float(input("Pris per enhet (eks. 149.90): "))
            if 0 < pris <= 99999.99:
                break
            else:
                print("Prisen må være over 0 og maks 99999.99 kr.")
        except ValueError:
            print("Ugyldig pris. Skriv et tall, f.eks. 199.50.")

    # Finn neste ledige varenummer
    høyeste_nummer = max([v["varenummer"] for v in data], default=0)
    varenummer = høyeste_nummer + 1

    ny_vare = {
        "varenummer": varenummer,
        "navn": navn,
        "kategori": kategori,
        "antall": antall,
        "pris": pris
    }

    data.append(ny_vare)
    write_data(data)
    print("✅ Varen er registrert.")
    input("\nTrykk Enter for å fortsette...")
    printMeny()


#Viser antall varer på lager vedlig 
def antallVarer():
    data = last_data()
    print("Antall varer på lager:")
    for vare in data:
        print(f"- {vare['navn']}: {vare['antall']} stk")
    input("\nTrykk Enter for å fortsette...")
    

#Søke en vare basert på kategori 
def søkVarer():
    data = last_data()
    søk = input("Skriv inn varenavn eller varenummer: ").strip().lower()

    if not søk:
        print("Du må skrive noe for å søke.")
        input("\nTrykk Enter for å fortsette...")
        printMeny()
        return

    funnet = False
    for vare in data:
        if søk in vare["navn"].lower() or søk == str(vare["varenummer"]):
            print(f"\n Fant vare: {vare['navn']} (#{vare['varenummer']})")
            print(f"Kategori: {vare['kategori']}")
            print(f"Antall: {vare['antall']} stk")
            print(f"Pris per enhet: {vare['pris']} kr")
            funnet = True
            break

    if not funnet:
        print("Fant ingen vare som matcher søket.")
    input("\nTrykk Enter for å fortsette...")
    printMeny()
    
#Søke etter en bestem kategori 
def visKategori():
    data = last_data()

    if not data:
        print("Lageret er tomt.")
        input("\nTrykk Enter for å fortsette...")
        printMeny()
        return

    kategori_input = input("Skriv inn navnet på kategorien du vil se: ").strip().lower()
    funnet = False

    print(f"\nVarer i kategorien '{kategori_input}':")
    for vare in data:
        if vare["kategori"].lower() == kategori_input:
            print(f"- {vare['navn']} (#{vare['varenummer']}), Antall: {vare['antall']}, Pris: {vare['pris']} kr")
            funnet = True

    if not funnet:
        print("Fant ingen varer i den kategorien.")

    input("\nTrykk Enter for å fortsette...")
    printMeny()


#Lar deg oppdatere antall varer du kan legge til eller fjerne varer   
def OppdaterVarer():
    data = last_data()
    
    # Varenummer må være et gyldig heltall
    try:
        varenummer = int(input("Skriv inn varenummeret du vil oppdatere: "))
    except ValueError:
        print("Ugyldig varenummer. Du må skrive et heltall.")
        input("\nTrykk Enter for å fortsette...")
        printMeny()
        return

    funnet = False
    for vare in data:
        if vare["varenummer"] == varenummer:
            print(f"Varen du vil oppdatere er: {vare['navn']} (Antall nå: {vare['antall']})")

            # Endring må være et heltall, og resultatet kan ikke bli negativt
            while True:
                try:
                    endring = int(input("Hvor mange vil du legge til (+) eller trekke fra (-): "))
                    nytt_antall = vare["antall"] + endring
                    if nytt_antall < 0:
                        print("Du kan ikke få negativt antall på lager.")
                    else:
                        vare["antall"] = nytt_antall
                        break
                except ValueError:
                    print("Ugyldig antall. Du må skrive et heltall.")

            print(f"✅ Oppdatert antall: {vare['antall']} stk")
            funnet = True
            break

    if not funnet:
        print("Varenummeret finnes ikke.")

    write_data(data)
    input("\nTrykk Enter for å fortsette...")
    printMeny()

#Viser en oversikt over varene i lager systemet  
def lagerStatus():
    data = last_data()
    print("\n--- Lagerstatus ---")
    for vare in data:
        print(f"#{vare['varenummer']}: {vare['navn']} ({vare['kategori']})")
        print(f"   Antall: {vare['antall']} stk | Pris: {vare['pris']} kr")
    print("--------------------")
    input("\nTrykk Enter for å fortsette...")
    printMeny()
    
#Funksjon for å slette en produkt 
def slettVare():
    data = last_data()

    try:
        varenummer = int(input("Skriv inn varenummeret (kategori) til varen du vil slette: "))
    except ValueError:
        print("Ugyldig varenummer. Du må skrive et heltall.")
        input("\nTrykk Enter for å fortsette...")
        printMeny()
        return

    for vare in data:
        if vare["varenummer"] == varenummer:
            print(f"\nDu er i ferd med å slette: {vare['navn']} (#{vare['varenummer']})")
            bekreft = input("Er du sikker? (J/N): ").strip().lower()
            if bekreft == "j" or bekreft == "ja" or bekreft == "j":
                data.remove(vare)
                write_data(data)
                print(" Varen ble slettet fra lageret.")
            else:
                print("Sletting avbrutt.")
            break
    else:
        print("Fant ingen vare med det varenummeret.")

    input("\nTrykk Enter for å fortsette...")
    printMeny()


# Når programmet startes kjører menyen
if __name__ == "__main__":
    printMeny()




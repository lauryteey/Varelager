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
    
#Funksjon for å printe menyen og funksjoner til menyen 

def printMeny():
    print("------------------- Din varerlager -------------------")
    print("| 1. Registrer nye varer                              |")
    print("| 2. Vise antall varer på din lager                   |")
    print("| 3. søke etter varer                                 |")
    print("| 4. Oppdater antall varer ved inn -og utlevering     |")
    print("| 5. Rapport over lagerstatus                         |")
    print("| 6. Avslutt                                          |")
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
        OppdaterVarer()
    elif valgtTall == "5":
        lagerStatus()
    elif valgtTall == "6":
        bekreftelse = input("Er du sikker på at du vil avslutte? J/N ")
        if (bekreftelse == "J" or bekreftelse == "j" or bekreftelse == "ja"):
            exit()
    else:
        nyttForsoek = input("Ugyldig valg. Velg et tall mellom 1-6: ")
        utfoerMenyvalg(nyttForsoek)
        
        
#Funksjoner fra menyen 

def registrerVarer(): 
    data = last_data()
    navn = input("Navn på varen: ")
    kategori = input("Kategori: ")
    antall = int(input("Antall på lager: "))
    pris = float(input("Pris per enhet: "))
    
    # Finn neste ledige varenummer
    høyeste_nummer = 0
    for vare in data:
        if vare["varenummer"] > høyeste_nummer:
            høyeste_nummer = vare["varenummer"]
    
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
    print("✅ Varen er registrert. YAY!")
    printMeny()
    
def antallVarer():
    data = last_data()
    print("Antall varer på lager:")
    for vare in data:
        print(f"- {vare['navn']}: {vare['antall']} stk")
        
def søkVarer():
    data = last_data()
    søk = input("Vennligst skriv inn navn eller varet nummer: ").lower()
    
    funnet = False 
    
    for vare in data: 
        if søk in vare ["navn"].lower() or søk == str(vare["varenummer"]): 
            print(f"Fant vare: {vare['navn']} (#{vare['varenummer']})")
            print(f"Kategori: {vare['kategori']}")
            print(f"Antall: {vare['antall']}")
            print(f"Pris per enhet: {vare['pris']} kr")
            funnet = True
            break

    if not funnet:
        print("Fant ingen vare som matcher søket.")

    printMeny()
    
def OppdaterVarer():
    data = last_data()
    try:
        varenummer = int(input("Skriv inn varenummeret du vil oppdatere: "))
        funnet = False

        for vare in data:
            if vare["varenummer"] == varenummer:
                print(f"Varen du vil oppdatere er: {vare['navn']}")
                endring = int(input("Hvor mange vil du legge til (Skriv (+ 'nummer' ) for å legge til eller fjerne (- 'nummer' ) for å fjerne1? "))
                vare["antall"] += endring
                print(f" Nytt antall: {vare['antall']} stk")
                funnet = True
                break

        if not funnet:
            print("Varenummer ikke funnet. WOMP WOMP")

        write_data(data)

    except ValueError:
        print(" Ugyldig input. Du må skrive et tall din lille pung.")

    printMeny()
    
def lagerStatus():
    data = last_data()
    print("\n--- Lagerstatus ---")
    for vare in data:
        print(f"#{vare['varenummer']}: {vare['navn']} ({vare['kategori']})")
        print(f"   Antall: {vare['antall']} stk | Pris: {vare['pris']} kr")
    print("--------------------")
    printMeny()




if __name__ == "__main__":
    printMeny()




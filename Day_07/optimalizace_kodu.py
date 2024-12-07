from typing import List, Tuple, Set, Optional
from itertools import product
import re
from dataclasses import dataclass

@dataclass
class Rovnice:
    """Třída reprezentující jednu rovnici."""
    testovaci_hodnota: int
    cisla: List[int]

class OpravaMostu:
    def __init__(self, vstupni_data: List[str]):
        """Inicializace se vstupními daty."""
        self._surova_data = vstupni_data
        self._rovnice = self._zpracuj_vstup()
        self._operatory_cast1 = ['+', '*']
        self._operatory_cast2 = ['+', '*', '||']

    def _zpracuj_vstup(self) -> List[Rovnice]:
        """Parsování vstupních dat do seznamu rovnic."""
        rovnice = []
        for radek in self._surova_data:
            if not radek.strip():
                continue
            shoda = re.match(r'(\d+): (.*)', radek)
            if shoda:
                testovaci_hodnota = int(shoda.group(1))
                cisla = [int(x) for x in shoda.group(2).split()]
                rovnice.append(Rovnice(testovaci_hodnota, cisla))
        return rovnice

    def _vypocitej_vyraz(self, cisla: List[int], operatory: List[str]) -> int:
        """Vyhodnocení výrazu s danými operátory."""
        vysledek = cisla[0]
        for i, op in enumerate(operatory):
            if op == '+':
                vysledek += cisla[i + 1]
            elif op == '*':
                vysledek *= cisla[i + 1]
            else:  # op == '||'
                vysledek = int(str(vysledek) + str(cisla[i + 1]))
        return vysledek

    def _je_platna_rovnice(self, rovnice: Rovnice, seznam_operatoru: List[str]) -> bool:
        """Kontrola, zda lze rovnici vyřešit s danými operátory."""
        pocet_operatoru = len(rovnice.cisla) - 1
        
        for ops in product(seznam_operatoru, repeat=pocet_operatoru):
            try:
                vysledek = self._vypocitej_vyraz(rovnice.cisla, ops)
                if vysledek == rovnice.testovaci_hodnota:
                    return True
            except ValueError:
                continue
        return False

    def vyres_cast1(self) -> int:
        """Řešení první části úlohy."""
        platne_rovnice = []
        
        for rovnice in self._rovnice:
            if self._je_platna_rovnice(rovnice, self._operatory_cast1):
                platne_rovnice.append(rovnice.testovaci_hodnota)
        
        return sum(platne_rovnice)

    def vyres_cast2(self) -> int:
        """Řešení druhé části úlohy."""
        platne_rovnice = []
        
        for rovnice in self._rovnice:
            if self._je_platna_rovnice(rovnice, self._operatory_cast2):
                platne_rovnice.append(rovnice.testovaci_hodnota)
        
        return sum(platne_rovnice)

def nacti_data(nazev_souboru: str) -> str:
    """Načte vstupní data ze souboru."""
    try:
        with open(nazev_souboru, 'r') as soubor:
            return soubor.read().strip()
    except FileNotFoundError:
        print(f"Soubor {nazev_souboru} nebyl nalezen!")
        return ""
    except Exception as e:
        print(f"Nastala chyba při čtení souboru: {e}")
        return ""

def main():
    # Načtení dat
    nazev_souboru = "Day_07/input_07.txt"
    print(f"Načítám soubor: {nazev_souboru}")
    vstupni_data = nacti_data(nazev_souboru)
    
    if not vstupni_data:
        print("Nepodařilo se načíst vstupní data.")
        return
    
    # Zpracování dat
    data_mapy = [radek.strip() for radek in vstupni_data.strip().split('\n')]
    resitel = OpravaMostu(data_mapy)
    
    # Část 1
    print("\nŘeším část 1...")
    vysledek1 = resitel.vyres_cast1()
    print(f"VÝSLEDEK část 1: {vysledek1}")
    
    # Část 2
    print("\nŘeším část 2...")
    vysledek2 = resitel.vyres_cast2()
    print(f"VÝSLEDEK část 2: {vysledek2}")

    # Test na ukázkovém vstupu
    testovaci_vstup = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip().split('\n')

    print("\nTestuji na ukázkových datech:")
    testovaci_resitel = OpravaMostu(testovaci_vstup)
    test_vysledek1 = testovaci_resitel.vyres_cast1()
    test_vysledek2 = testovaci_resitel.vyres_cast2()
    print(f"Test část 1: {test_vysledek1}")  # Mělo by být 3749
    print(f"Test část 2: {test_vysledek2}")  # Mělo by být 11387

if __name__ == "__main__":
    main()
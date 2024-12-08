import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt

def nacti_mapu(nazev_souboru):
    """Načte mapu ze souboru a vrátí ji jako seznam seznamů"""
    with open(nazev_souboru, 'r') as soubor:
        radky = soubor.readlines()
    return [list(radek.strip()) for radek in radky]

def najdi_anteny(mapa):
    """
    Najde všechny antény v mapě a vrátí je seskupené podle frekvence
    Returns: slovník kde klíč je frekvence a hodnota je seznam souřadnic antén
    """
    anteny = defaultdict(list)
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x] != '.':
                anteny[mapa[y][x]].append((x, y))
    return anteny

def najdi_pary_anten(mapa):
    """
    Najde všechny páry antén se stejnou frekvencí
    Returns: slovník kde klíč je frekvence a hodnota je seznam souřadnic antén (pouze pro frekvence s 2 a více anténami)
    """
    anteny = defaultdict(list)
    
    # Projdu mapu a najdu všechny antény
    for y in range(len(mapa)):
        for x in range(len(mapa[0])):
            if mapa[y][x] != '.':
                anteny[mapa[y][x]].append((x, y))
    
    # Vrátím jen ty frekvence, kde mám 2 a více antén
    return {freq: pozice for freq, pozice in anteny.items() if len(pozice) >= 2}

def vypocitej_antinody(antena1, antena2, sirka_mapy, vyska_mapy):
    """
    Vypočítá antinody pro pár antén podle pravidla 1:2
    Antinody jsou ve vzdálenosti 1x a 2x vektor od každé antény
    """
    x1, y1 = antena1
    x2, y2 = antena2
    
    # Vypočítám vektor mezi anténami (jak daleko jsou od sebe v osách x a y)
    dx = x2 - x1
    dy = y2 - y1
    
    antinody = []
    
    # První antinoda - jdu PROTI směru vektoru od první antény
    antinoda1_x = x1 - dx
    antinoda1_y = y1 - dy
    
    # Druhá antinoda - jdu VE směru vektoru od druhé antény
    antinoda2_x = x2 + dx
    antinoda2_y = y2 + dy
    
    # Kontrola, jestli jsou antinody v mapě
    if 0 <= antinoda1_x < sirka_mapy and 0 <= antinoda1_y < vyska_mapy:
        antinody.append((int(antinoda1_x), int(antinoda1_y)))
        # print(f"Antinoda 1 pro {antena1}-{antena2}: {(antinoda1_x, antinoda1_y)} je v mapě")
    # else:
        # print(f"Antinoda 1 pro {antena1}-{antena2}: {(antinoda1_x, antinoda1_y)} je mimo mapu")
    
    if 0 <= antinoda2_x < sirka_mapy and 0 <= antinoda2_y < vyska_mapy:
        antinody.append((int(antinoda2_x), int(antinoda2_y)))
        # print(f"Antinoda 2 pro {antena1}-{antena2}: {(antinoda2_x, antinoda2_y)} je v mapě")
    # else:
        # print(f"Antinoda 2 pro {antena1}-{antena2}: {(antinoda2_x, antinoda2_y)} je mimo mapu")
    
    return antinody

def vykresli_mapu(mapa, antinody, pary_anten, cislo_grafu, titulek):
    """Vykreslí mapu s anténami, spojnicemi párů a antinodami"""
    plt.subplot(1, 2, cislo_grafu)  # Použijeme subplot místo nové figure
    
    vyska = len(mapa)
    sirka = len(mapa[0])
    
    # Vykreslím mřížku
    for i in range(sirka + 1):
        plt.axvline(x=i, color='gray', linewidth=0.5, alpha=0.3)
    for i in range(vyska + 1):
        plt.axhline(y=i, color='gray', linewidth=0.5, alpha=0.3)
    
    # Vykreslím antény
    for y in range(vyska):
        for x in range(sirka):
            if mapa[y][x] != '.':
                plt.text(x, y, mapa[y][x], 
                        ha='center', va='center', color='blue')
    
    # Vykreslím spojnice párů antén
    barvy = plt.cm.rainbow(np.linspace(0, 1, len(pary_anten)))
    for (frekvence, pozice), barva in zip(pary_anten.items(), barvy):
        for i in range(len(pozice)):
            for j in range(i + 1, len(pozice)):
                ant1 = pozice[i]
                ant2 = pozice[j]
                plt.plot([ant1[0], ant2[0]], [ant1[1], ant2[1]], '--', 
                        color=barva, alpha=0.5)
    
    # Vykreslím antinody
    for x, y in antinody:
        plt.plot(x, y, 'r*', markersize=15)
    
    plt.grid(True)
    plt.xlim(-0.5, sirka - 0.5)
    plt.ylim(-0.5, vyska - 0.5)
    plt.title(titulek)
    plt.gca().set_aspect('equal', adjustable='box')

def jsou_v_primce(bod1, bod2, bod3):
    """
    Kontrola jestli tři body leží na přímce
    Používá vektorový součin - když je nulový, body jsou v přímce
    """
    x1, y1 = bod1
    x2, y2 = bod2
    x3, y3 = bod3
    
    return (y2 - y1) * (x3 - x1) == (y3 - y1) * (x2 - x1)

def najdi_body_na_primce(antena1, antena2, sirka_mapy, vyska_mapy):
    """Najde všechny body na přímce mezi dvěma anténami, které jsou v mapě"""
    x1, y1 = antena1
    x2, y2 = antena2
    
    body = set()
    
    # Pro antény ve stejném řádku
    if y1 == y2:
        for x in range(sirka_mapy):
            body.add((x, y1))
    
    # Pro antény ve stejném sloupci
    elif x1 == x2:
        for y in range(vyska_mapy):
            body.add((x1, y))
    
    # Pro šikmé přímky
    else:
        # Projdu všechny možné body v mapě
        for x in range(sirka_mapy):
            for y in range(vyska_mapy):
                if jsou_v_primce(antena1, antena2, (x, y)):
                    body.add((x, y))
    
    return body

def vypocitej_harmonicke_antinody(mapa):
    """Vypočítá všechny harmonické antinody pro Part 2"""
    anteny = najdi_anteny(mapa)
    vsechny_antinody = set()
    
    vyska = len(mapa)
    sirka = len(mapa[0])
    
    # Pro každou frekvenci najdu antinody
    for frekvence, pozice in anteny.items():
        # Pro každý pár antén stejné frekvence
        for i in range(len(pozice)):
            for j in range(i + 1, len(pozice)):
                antena1 = pozice[i]
                antena2 = pozice[j]
                
                # Najdu všechny body na přímce mezi anténami
                body_na_primce = najdi_body_na_primce(antena1, antena2, sirka, vyska)
                vsechny_antinody.update(body_na_primce)
    
    return vsechny_antinody

def main():
    # Načtu mapu
    mapa = nacti_mapu("Day_08/input_08.txt")
    vyska = len(mapa)
    sirka = len(mapa[0])
    
    # Part 1 - antinody podle pravidla 1:2
    pary_anten = najdi_pary_anten(mapa)
    antinody_cast1 = set()
    
    for frekvence, pozice in pary_anten.items():
        for i in range(len(pozice)):
            for j in range(i + 1, len(pozice)):
                antena1 = pozice[i]
                antena2 = pozice[j]
                antinody = vypocitej_antinody(antena1, antena2, sirka, vyska)
                antinody_cast1.update(antinody)
    
    # Part 2 - harmonické antinody
    antinody_cast2 = vypocitej_harmonicke_antinody(mapa)
    
    print(f"\nVýsledky:")
    print(f"Part 1 - Počet antinod (pravidlo 1:2): {len(antinody_cast1)}")
    print(f"Part 2 - Počet harmonických antinod: {len(antinody_cast2)}")
    
    # Vykreslení obou řešení v jednom okně
    plt.figure(figsize=(20, 10))
    
    # Part 1
    vykresli_mapu(mapa, antinody_cast1, pary_anten, 1, 'Part 1 - Antinody podle pravidla 1:2')
    
    # Part 2
    vykresli_mapu(mapa, antinody_cast2, pary_anten, 2, 'Part 2 - Harmonické antinody')
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
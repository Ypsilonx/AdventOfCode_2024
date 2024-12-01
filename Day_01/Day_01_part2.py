sloupec1 = []
sloupec2 = []

with open('Day_01/input_01.txt', 'r') as file:
    for line in file:
        cisla = line.split()
        
        if len(cisla) >= 2:
            sloupec1.append(int(cisla[0]))
            sloupec2.append(int(cisla[1]))

def vytvorit_slovo_po_uziv_nalezu(sloupec1, sloupec2):
    slovnik = {}

    for cislo in sloupec1:
        pocet_vyskytu = sloupec2.count(cislo)
        slovnik[cislo] = cislo * pocet_vyskytu

    return slovnik

def secti_items_ze_slovniku(slovnik):
    celkova_soucet = sum(slovnik.values()) 
    return celkova_soucet

slovnik = vytvorit_slovo_po_uziv_nalezu(sloupec1, sloupec2)
celkova_soucet = secti_items_ze_slovniku(slovnik)
print("Celkový součet:", celkova_soucet)

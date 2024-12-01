sloupec1 = []
sloupec2 = []

with open('Day_01/input_01.txt', 'r') as file:
    for line in file:
        cisla = line.split()
        
        if len(cisla) >= 2:
            sloupec1.append(int(cisla[0]))  # Převod na číslo (float)
            sloupec2.append(int(cisla[1]))  # Převod na číslo (float)

def najit_pary_a_vypocitat_rozdily(sloupec1, sloupec2):
    pary = []
    rozdily = []

    sloupec1 = sorted((value, index) for index, value in enumerate(sloupec1))
    sloupec2 = sorted((value, index) for index, value in enumerate(sloupec2))
    
    while sloupec1 and sloupec2:
        nejmensi_cislo_sloupec1, index1 = sloupec1.pop(0)
        nejmensi_cislo_sloupec2, index2 = sloupec2.pop(0)
        
        if nejmensi_cislo_sloupec1 < nejmensi_cislo_sloupec2:
            rozdil = nejmensi_cislo_sloupec2 - nejmensi_cislo_sloupec1
            pary.append((nejmensi_cislo_sloupec1, nejmensi_cislo_sloupec2))
            rozdily.append(rozdil)
        else:
            rozdil = nejmensi_cislo_sloupec1 - nejmensi_cislo_sloupec2
            pary.append((nejmensi_cislo_sloupec2, nejmensi_cislo_sloupec1))
            rozdily.append(rozdil)
                
    return pary, rozdily

pary, rozdily = najit_pary_a_vypocitat_rozdily(sloupec1, sloupec2)
print("Součet rozdílů:", sum(rozdily))
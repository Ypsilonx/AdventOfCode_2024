from itertools import product
import re

def parsovani(line):
    """Rozdělí mi vstupní data."""
    reg_shoda = re.match(r'(\d+): (.*)', line)
    if reg_shoda:
        test_value = int(reg_shoda.group(1))
        cisla = [int(x) for x in reg_shoda.group(2).split()]
        return test_value, cisla
    return None

def vyhodnoceni_vyrazu(cisla, operatory):
    """Vyhodnotí vyraz které operatory použit."""
    result = cisla[0]
    for i, op in enumerate(operatory):
        if op == '+':
            result += cisla[i + 1]
        elif op == '*':
            result *= cisla[i + 1]
        else:  # op == '||'
            result = int(str(result) + str(cisla[i + 1]))
    return result

def najdi_spravne_rovnice(mozne_rovnice):
    """Find mozne_rovnice that can be solved with +, * and || operator."""
    spravne_rovnice = []
    
    for test_value, cisla in mozne_rovnice:
        num_operatory = len(cisla) - 1
        
        for ops in product(['+', '*', '||'], repeat=num_operatory):
            try:
                result = vyhodnoceni_vyrazu(cisla, ops)
                if result == test_value:
                    spravne_rovnice.append(test_value)
                    break
            except ValueError:
                continue
                
    return spravne_rovnice

def vyreseni_opravy_mostu(input_text):
    """Hlavní funkce pro řešení."""
    mozne_rovnice = []
    for line in input_text.strip().split('\n'):
        if line: 
            parsed = parsovani(line)
            if parsed:
                mozne_rovnice.append(parsed)
                
    spravne_rovnice = najdi_spravne_rovnice(mozne_rovnice)
    total = sum(spravne_rovnice)
    print(f"Nalezeno {len(spravne_rovnice)} správných rovnic.")
    return total

test_input = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
print("\nTestovací data:")
test_result = vyreseni_opravy_mostu(test_input)
print(f"Výsledek testování: {test_result}")

file_path = "Day_07/input_07.txt"
try:
    with open(file_path, 'r') as file:
        input_data = file.read()
    result = vyreseni_opravy_mostu(input_data)
    print(f"Kalibrační data: {result}")
except FileNotFoundError:
    print(f"Chyba: Soubor {file_path} nebyl nenalezen!")
except Exception as e:
    print(f"ERROR: {e}")

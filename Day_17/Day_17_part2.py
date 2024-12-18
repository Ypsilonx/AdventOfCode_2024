class ThreeBitComputer:
    def __init__(self, register_a=0, register_b=0, register_c=0):
        self.reset_registers(register_a, register_b, register_c)
        self.outputs = []
        self.instruction_pointer = 0
    
    def reset_registers(self, register_a=0, register_b=0, register_c=0):
        """Reset registrů na počáteční hodnoty"""
        self.registers = {'A': register_a, 'B': register_b, 'C': register_c}
        self.outputs = []
        self.instruction_pointer = 0

    def get_combo_value(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError("Neplatný combo operand")

    def run_instruction(self, opcode, operand):
        if opcode == 0:  
            power = self.get_combo_value(operand)
            self.registers['A'] //= (2 ** power)
            self.instruction_pointer += 2
            
        elif opcode == 1:  
            self.registers['B'] ^= operand
            self.instruction_pointer += 2
            
        elif opcode == 2:  
            self.registers['B'] = self.get_combo_value(operand) % 8
            self.instruction_pointer += 2
            
        elif opcode == 3:  
            if self.registers['A'] != 0:
                self.instruction_pointer = operand
            else:
                self.instruction_pointer += 2
                
        elif opcode == 4:  
            self.registers['B'] ^= self.registers['C']
            self.instruction_pointer += 2
            
        elif opcode == 5: 
            output_value = self.get_combo_value(operand) % 8
            self.outputs.append(str(output_value))
            self.instruction_pointer += 2
            
        elif opcode == 6:  
            power = self.get_combo_value(operand)
            self.registers['B'] = self.registers['A'] // (2 ** power)
            self.instruction_pointer += 2
            
        elif opcode == 7: 
            power = self.get_combo_value(operand)
            self.registers['C'] = self.registers['A'] // (2 ** power)
            self.instruction_pointer += 2

    def run_program(self, program):
        if isinstance(program, str):
            program = [int(x.strip()) for x in program.split(',')]
        
        self.outputs = []
        self.instruction_pointer = 0
        
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]
            self.run_instruction(opcode, operand)
        
        return ','.join(self.outputs)

def find_solution(program, start_value=630000000, max_attempts=1000000000):
    """
    Hledá nejmenší kladné číslo pro registr A, které způsobí,
    že program vypíše sám sebe
    """
    computer = ThreeBitComputer()
    target_output = program  
    
    print(f"Hledám řešení pro program: {program}")
    print(f"Cílový výstup: {target_output}")
    
    for a in range(start_value, start_value + max_attempts):
        if a % 10000 == 0:  
            print(f"Zkouším hodnotu A: {a}")
            
        computer.reset_registers(register_a=a)
        output = computer.run_program(program)
        
        if output == target_output:
            print(f"Nalezeno řešení! A = {a}")
            print(f"Výstup: {output}")
            print(f"Očekáváno: {target_output}")
            return a
            
    print("Řešení nebylo nalezeno v daném rozsahu")
    return None

if __name__ == "__main__":
    program = "2,4,1,1,7,5,1,4,0,3,4,5,5,5,3,0"
    solution = find_solution(program)
    print(f"Výsledek: {solution}")
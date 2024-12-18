class ThreeBitComputer:
    def __init__(self, register_a=0, register_b=0, register_c=0):
        self.registers = {
            'A': register_a,
            'B': register_b,
            'C': register_c
        }
        self.outputs = []
        self.instruction_pointer = 0

    def get_combo_value(self, operand):
        """
        Získá hodnotu operandu podle pravidel pro combo operandy:
        0-3: přímo hodnota
        4-6: hodnota z registru A/B/C
        7: rezervováno (nepoužívá se)
        """
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
        """
        Zpracuje jednu instrukci podle jejího opcode a operandu
        """
        if opcode == 0:  # adv - dělení do A
            power = self.get_combo_value(operand)
            self.registers['A'] //= (2 ** power)
            self.instruction_pointer += 2
            
        elif opcode == 1:  # bxl - XOR B s literálem
            self.registers['B'] ^= operand
            self.instruction_pointer += 2
            
        elif opcode == 2:  # bst - uložení do B
            self.registers['B'] = self.get_combo_value(operand) % 8
            self.instruction_pointer += 2
            
        elif opcode == 3:  # jnz - skok pokud A není 0
            if self.registers['A'] != 0:
                self.instruction_pointer = operand
            else:
                self.instruction_pointer += 2
                
        elif opcode == 4:  # bxc - XOR B s C
            self.registers['B'] ^= self.registers['C']
            self.instruction_pointer += 2
            
        elif opcode == 5:  # out - výstup
            output_value = self.get_combo_value(operand) % 8
            self.outputs.append(str(output_value))
            self.instruction_pointer += 2
            
        elif opcode == 6:  # bdv - dělení do B
            power = self.get_combo_value(operand)
            self.registers['B'] = self.registers['A'] // (2 ** power)
            self.instruction_pointer += 2
            
        elif opcode == 7:  # cdv - dělení do C
            power = self.get_combo_value(operand)
            self.registers['C'] = self.registers['A'] // (2 ** power)
            self.instruction_pointer += 2

    def run_program(self, program):
        """
        Spustí celý program - seznam instrukcí
        """
        if isinstance(program, str):
            program = [int(x.strip()) for x in program.split(',')]
        
        while self.instruction_pointer < len(program):
            opcode = program[self.instruction_pointer]
            operand = program[self.instruction_pointer + 1]
            self.run_instruction(opcode, operand)
        
        return ','.join(self.outputs)

if __name__ == "__main__":
    computer = ThreeBitComputer(
        register_a=0000000,
        register_b=0,
        register_c=0
    )
    
    program = "ZDE VAS KOD"
    
    result = computer.run_program(program)
    print(f"Výstup programu: {result}")
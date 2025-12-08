import sys

class MathAutomata:
    def __init__(self):
        # Definisi Operator dan Prioritas (Precedence)
        self.operators = {'+', '-', '*', '/'}
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    def is_operand(self, token):
        """Mengecek apakah token adalah angka (digit)"""
        return token.isalnum()

    # --- BAGIAN 1: VALIDATOR (Logic PDA/State Machine) ---
    def validate(self, expression, type_mode):
        """
        Memvalidasi ekspresi berdasarkan mode (Infix, Postfix, Prefix).
        Menggunakan konsep counter stack untuk simulasi automata.
        """
        tokens = expression.split()
        if not tokens:
            return False, "Input kosong."

        if type_mode == "infix":
            # Infix: Harus selang-seling (Operand -> Operator -> Operand)
            state = 'EXPECT_OPERAND' # q0
            paren_balance = 0
            
            for token in tokens:
                if self.is_operand(token):
                    if state == 'EXPECT_OPERAND': state = 'EXPECT_OPERATOR'
                    else: return False, "Infix Error: Mengharapkan operator, dapat operand."
                elif token in self.operators:
                    if state == 'EXPECT_OPERATOR': state = 'EXPECT_OPERAND'
                    else: return False, "Infix Error: Mengharapkan operand, dapat operator."
                elif token == '(':
                    if state == 'EXPECT_OPERATOR': return False, "Infix Error: Kurung buka salah tempat."
                    paren_balance += 1
                elif token == ')':
                    if state == 'EXPECT_OPERAND': return False, "Infix Error: Kurung tutup salah tempat."
                    paren_balance -= 1
                else:
                    return False, f"Token tidak dikenal: {token}"
            
            if paren_balance != 0: return False, "Infix Error: Tanda kurung tidak lengkap."
            if state == 'EXPECT_OPERAND': return False, "Infix Error: Berakhir dengan operator."
            return True, "Valid Infix"

        elif type_mode == "postfix":
            stack_count = 0 
            for token in tokens:
                if self.is_operand(token):
                    stack_count += 1
                elif token in self.operators:
                    if stack_count < 2: return False, "Postfix Error: Operand tidak cukup untuk operator."
                    stack_count -= 1 # Mengurangi 1 net value (Pop 2, Push 1)
            
            if stack_count == 1: return True, "Valid Postfix"
            return False, "Postfix Error: Terlalu banyak operand tersisa."

        elif type_mode == "prefix":
            # Prefix: Sama kayak Postfix tapi scan dari Kanan ke Kiri (Reversed)
            stack_count = 0
            for token in reversed(tokens):
                if self.is_operand(token):
                    stack_count += 1
                elif token in self.operators:
                    if stack_count < 2: return False, "Prefix Error: Operand tidak cukup."
                    stack_count -= 1
            
            if stack_count == 1: return True, "Valid Prefix"
            return False, "Prefix Error: Struktur tidak valid."
        
        return False, "Mode tidak dikenal."

    # --- BAGIAN 2: CONVERTER (Logic Stack Processing) ---
    def infix_to_postfix(self, expression):
        stack = []
        output = []
        tokens = expression.split()

        for token in tokens:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop() # Buang '('
            elif token in self.operators:
                while (stack and stack[-1] != '(' and 
                    self.precedence.get(token, 0) <= self.precedence.get(stack[-1], 0)):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        return " ".join(output)

    def postfix_to_infix(self, expression):
        stack = []
        tokens = expression.split()
        for token in tokens:
            if self.is_operand(token):
                stack.append(token)
            else:
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(f"({op1} {token} {op2})")
        return stack[0]

    def prefix_to_infix(self, expression):
        stack = []
        tokens = expression.split()
        # Prefix diproses dari belakang ke depan
        for token in reversed(tokens):
            if self.is_operand(token):
                stack.append(token)
            else:
                op1 = stack.pop()
                op2 = stack.pop()
                stack.append(f"({op1} {token} {op2})")
        return stack[0]

    # Fungsi Hub (Pusat): Menggunakan Infix sebagai perantara
    def convert(self, expression, from_type, to_type):
        # 1. Validasi dulu
        is_valid, msg = self.validate(expression, from_type)
        if not is_valid:
            return f"GAGAL: {msg}"

        # 2. Normalisasi ke Infix dulu (Intermediate Representation)
        infix_val = ""
        if from_type == "infix": infix_val = expression
        elif from_type == "postfix": infix_val = self.postfix_to_infix(expression)
        elif from_type == "prefix": infix_val = self.prefix_to_infix(expression)

        # 3. Konversi dari Infix ke Target
        if to_type == "infix": return infix_val
        elif to_type == "postfix": return self.infix_to_postfix(infix_val)
        elif to_type == "prefix":
            rev_infix = infix_val[::-1].replace('(', 'TEMP').replace(')', '(').replace('TEMP', ')')
            return self._infix_to_prefix_logic(infix_val)

    def _infix_to_prefix_logic(self, infix_expr):
        # Algoritma: Reverse Infix -> Swap Kurung -> Postfix -> Reverse Result
        tokens = infix_expr.split()
        tokens = tokens[::-1]
        
        swapped_tokens = []
        for t in tokens:
            if t == '(': swapped_tokens.append(')')
            elif t == ')': swapped_tokens.append('(')
            else: swapped_tokens.append(t)
        
        # Pakai logic postfix
        temp_stack = []
        output = []
        
        # Logic Postfix tapi precedence 'Strict Less' untuk right associative
        for token in swapped_tokens:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                temp_stack.append(token)
            elif token == ')':
                while temp_stack and temp_stack[-1] != '(':
                    output.append(temp_stack.pop())
                temp_stack.pop()
            elif token in self.operators:
                # Perhatikan precedence
                while (temp_stack and temp_stack[-1] != '(' and 
                    self.precedence.get(token) < self.precedence.get(temp_stack[-1])): # < instead of <=
                    output.append(temp_stack.pop())
                temp_stack.append(token)
        
        while temp_stack:
            output.append(temp_stack.pop())
        
        return " ".join(output[::-1])


# --- BAGIAN 3: USER INTERFACE (Main Program) ---
def main():
    automata = MathAutomata()
    
    print("="*50)
    print(" TUGAS KELOMPOK: COMPILATION TECHNIQUES (SOAL 1)")
    print(" Automata Validator & Converter (OOP)")
    print("="*50)
    print("Catatan: Gunakan SPASI sebagai pemisah antar elemen.")
    print("Contoh Infix  : 3 + 5 * 2")
    print("Contoh Postfix: 3 5 2 * +")
    print("Contoh Prefix : + 3 * 5 2")
    print("-" * 50)

    while True:
        print("\n--- MENU UTAMA ---")
        print("1. Input Rumus Baru")
        print("2. Keluar")
        
        pilihan = input("Pilih (1/2): ")
        if pilihan == '2':
            print("Program Selesai.")
            break
        
        if pilihan == '1':
            rumus = input("\nMasukkan Rumus Matematika: ").strip()
            
            print("\nPilih Format Input Asal:")
            print("a. Infix (Contoh: A + B)")
            print("b. Postfix (Contoh: A B +)")
            print("c. Prefix (Contoh: + A B)")
            src_choice = input("Pilihan (a/b/c): ").lower()
            
            map_type = {'a': 'infix', 'b': 'postfix', 'c': 'prefix'}
            if src_choice not in map_type:
                print("Pilihan salah!")
                continue
            
            src_type = map_type[src_choice]
            
            # Validasi dulu
            valid, msg = automata.validate(rumus, src_type)
            if not valid:
                print(f"\n[ERROR] Input tidak valid untuk format {src_type.upper()}!")
                print(f"Penyebab: {msg}")
                continue
            else:
                print(f"\n[OK] Validasi Berhasil: {msg}")

            print(f"\nIngin dikonversi ke format apa?")
            print("1. Infix")
            print("2. Postfix")
            print("3. Prefix")
            dest_choice = input("Pilihan (1/2/3): ")
            
            map_dest = {'1': 'infix', '2': 'postfix', '3': 'prefix'}
            if dest_choice not in map_dest:
                print("Pilihan salah!")
                continue
                
            dest_type = map_dest[dest_choice]
            
            hasil = automata.convert(rumus, src_type, dest_type)
            
            print("\n" + "*"*30)
            print(f"HASIL KONVERSI ({src_type} -> {dest_type}):")
            print(f"{hasil}")
            print("*"*30)

if __name__ == "__main__":
    main()
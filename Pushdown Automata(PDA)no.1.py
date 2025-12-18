import streamlit as st
import re

# ==========================================
# BAGIAN 1: LOGIC (BACKEND - AUTOMATA & OOP)
# ==========================================
class MathAutomata:
    def __init__(self):
        self.operators = {'+', '-', '*', '/', '^'}
        # Presedensi: ^ > * / > + -
        self.precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}

    def _tokenize(self, expression):
        """
        Lexical Analyzer: Menggunakan Regex untuk memisahkan token
        bahkan jika input tidak pakai spasi. Contoh: (3+5) -> ['(', '3', '+', '5', ')']
        """
        # Regex logic: Cari angka (digit) ATAU operator/kurung
        return re.findall(r"\d+|[+\-*/^()]", expression)

    def is_operand(self, token):
        return token.isdigit()

    def validate(self, expression, type_mode):
        tokens = self._tokenize(expression)
        if not tokens:
            return False, "Input kosong."

        if type_mode == "Infix":
            state = 'EXPECT_OPERAND' # State q0
            paren_balance = 0
            
            for token in tokens:
                if self.is_operand(token):
                    if state == 'EXPECT_OPERAND': state = 'EXPECT_OPERATOR'
                    else: return False, f"Error di '{token}': Mengharapkan operator."
                elif token in self.operators:
                    if state == 'EXPECT_OPERATOR': state = 'EXPECT_OPERAND'
                    else: return False, f"Error di '{token}': Mengharapkan operand."
                elif token == '(':
                    if state == 'EXPECT_OPERATOR': return False, "Error: Kurung buka salah posisi."
                    paren_balance += 1
                elif token == ')':
                    if state == 'EXPECT_OPERAND': return False, "Error: Kurung tutup salah posisi."
                    paren_balance -= 1
                else:
                    return False, f"Token ilegal: {token}"
            
            if paren_balance != 0: return False, "Error: Jumlah kurung tidak seimbang."
            if state == 'EXPECT_OPERAND': return False, "Error: Rumus menggantung (berakhir operator)."
            return True, "Valid Infix Expression"

        elif type_mode == "Postfix":
            stack_count = 0 
            for token in tokens:
                if self.is_operand(token): stack_count += 1
                elif token in self.operators:
                    if stack_count < 2: return False, "Error: Operand kurang."
                    stack_count -= 1
            return (True, "Valid Postfix") if stack_count == 1 else (False, "Error: Struktur salah.")

        elif type_mode == "Prefix":
            stack_count = 0
            for token in reversed(tokens):
                if self.is_operand(token): stack_count += 1
                elif token in self.operators:
                    if stack_count < 2: return False, "Error: Operand kurang."
                    stack_count -= 1
            return (True, "Valid Prefix") if stack_count == 1 else (False, "Error: Struktur salah.")
        
        return False, "Mode Error"

    def infix_to_postfix(self, expression):
        tokens = self._tokenize(expression)
        stack = []
        output = []
        
        for token in tokens:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack: stack.pop() # Buang '('
            elif token in self.operators:
                while (stack and stack[-1] != '(' and 
                       self.precedence.get(token, 0) <= self.precedence.get(stack[-1], 0)):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack:
            output.append(stack.pop())
        return " ".join(output)

    def postfix_to_infix(self, expression):
        tokens = self._tokenize(expression)
        stack = []
        for token in tokens:
            if self.is_operand(token):
                stack.append(token)
            else:
                if len(stack) < 2: return "Error"
                op2 = stack.pop()
                op1 = stack.pop()
                stack.append(f"({op1} {token} {op2})")
        return stack[0] if stack else ""

    def _infix_to_prefix_logic(self, infix_expr):
        # Reverse Infix -> Swap Kurung -> Postfix -> Reverse Result
        tokens = self._tokenize(infix_expr)
        tokens = tokens[::-1]
        swapped = ['(' if t == ')' else ')' if t == '(' else t for t in tokens]
        
        stack = []
        output = []
        for token in swapped:
            if self.is_operand(token):
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                if stack: stack.pop()
            elif token in self.operators:
                # Perhatikan: Strict less (<) untuk reverse logic
                while (stack and stack[-1] != '(' and 
                       self.precedence.get(token) < self.precedence.get(stack[-1])):
                    output.append(stack.pop())
                stack.append(token)
        
        while stack: output.append(stack.pop())
        return " ".join(output[::-1])

    def convert(self, expression, from_type, to_type):
        is_valid, msg = self.validate(expression, from_type)
        if not is_valid: return None, msg

        # Step 1: Normalize to Infix
        infix_val = ""
        if from_type == "Infix": infix_val = expression
        elif from_type == "Postfix": infix_val = self.postfix_to_infix(expression)
        elif from_type == "Prefix": 
            # Prefix to Infix logic
            stack = []
            for token in reversed(self._tokenize(expression)):
                if self.is_operand(token): stack.append(token)
                else:
                    if len(stack) < 2: return None, "Stack Error"
                    op1 = stack.pop()
                    op2 = stack.pop()
                    stack.append(f"({op1} {token} {op2})")
            infix_val = stack[0]

        # Step 2: Convert Infix to Target
        if to_type == "Infix": return infix_val, "Success"
        elif to_type == "Postfix": return self.infix_to_postfix(infix_val), "Success"
        elif to_type == "Prefix": return self._infix_to_prefix_logic(infix_val), "Success"

# ==========================================
# BAGIAN 2: TAMPILAN (FRONTEND - STREAMLIT)
# ==========================================

# Konfigurasi Halaman
st.set_page_config(page_title="Automata Converter", page_icon="🧮", layout="centered")

# Inisialisasi Class
automata = MathAutomata()

# Header
st.title("🧮 Math Automata Converter")
st.markdown("### Tugas Kelompok: Compilation Techniques")
st.markdown("Program validasi dan konversi rumus matematika berbasis **Pushdown Automata**.")
st.divider()

# Input User
col1, col2 = st.columns(2)

with col1:
    src_type = st.selectbox("Format Input (Asal)", ["Infix", "Postfix", "Prefix"])

with col2:
    dest_type = st.selectbox("Format Output (Tujuan)", ["Infix", "Postfix", "Prefix"], index=1)

# Input Rumus
rumus_input = st.text_input("Masukkan Rumus Matematika:", placeholder="Contoh: 3 + 5 * ( 2 - 8 )")
st.caption("Tips: Program sudah mendukung Regex, jadi spasi tidak wajib. Contoh: `(3+5)` aman.")

# Tombol Aksi
if st.button("🚀 Validasi & Konversi", type="primary"):
    if not rumus_input:
        st.warning("Mohon masukkan rumus terlebih dahulu.")
    else:
        # Proses 1: Validasi
        is_valid, valid_msg = automata.validate(rumus_input, src_type)
        
        if is_valid:
            st.success(f"✅ **VALIDASI SUKSES:** {valid_msg}")
            
            # Proses 2: Konversi
            hasil, status_msg = automata.convert(rumus_input, src_type, dest_type)
            
            if hasil:
                st.divider()
                st.subheader("Hasil Konversi:")
                
                # Menampilkan hasil dalam kotak yang cantik
                st.info(f"Dari **{src_type}** ke **{dest_type}**")
                st.code(hasil, language="text")
                
                # Visualisasi Stack (Simulasi Sederhana untuk Bonus Presentasi)
                with st.expander("Lihat Detail Tokenizing (Lexical Analysis)"):
                    tokens = automata._tokenize(rumus_input)
                    st.write("Program memecah input menjadi token berikut:")
                    st.write(tokens)
            else:
                st.error(f"❌ Konversi Gagal: {status_msg}")
        else:
            st.error(f"⛔ **INPUT TIDAK VALID**")
            st.error(f"Penyebab: {valid_msg}")
            # Tampilkan tips debugging
            if src_type == "Infix":
                st.markdown("""
                **Syarat Infix:**
                * Harus selang-seling Angka & Operator.
                * Kurung buka/tutup harus seimbang.
                * Tidak boleh operator di awal/akhir.
                """)

# Footer
st.divider()
st.markdown("<center><small>Dibuat oleh Kelompok Compilation Techniques • Binus University</small></center>", unsafe_allow_html=True)
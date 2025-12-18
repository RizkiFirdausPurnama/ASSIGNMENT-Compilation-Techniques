import tkinter as tk
from tkinter import ttk
import time
import json
import os
import platform

# --- KONFIGURASI WARNA & STYLE ---
BG_COLOR = "#1e1e2e"        # Background Utama
SIDEBAR_COLOR = "#181825"   # Background Menu Kiri (Lebih gelap)
TEXT_COLOR = "#cdd6f4"      # Teks Putih
ACCENT_COLOR = "#f38ba8"    # Merah (Error)
SUCCESS_COLOR = "#a6e3a1"   # Hijau (Sukses)
BOX_COLOR = "#313244"       # Kotak Input
BTN_COLOR = "#89b4fa"       # Tombol Normal
BTN_ACTIVE = "#a6e3a1"      # Tombol saat dipilih (Hijau)

class ComboEngine:
    def __init__(self, combo_file, target_combo_name=None):
        self.combo_file = combo_file
        self.target_combo_name = target_combo_name
        self.combos = self.load_combos()
        self.reset_state()

    def load_combos(self):
        if not os.path.exists(self.combo_file):
            return []
        try:
            with open(self.combo_file, 'r') as f:
                data = json.load(f)
            # Filter hanya combo yang dipilih
            if self.target_combo_name:
                return [c for c in data if c['name'] == self.target_combo_name]
            return data
        except Exception as e:
            print(f"Error: {e}")
            return []

    def reset_state(self):
        self.current_sequence = []
        self.last_input_time = time.time()
        self.possible_combos = self.combos[:]

    def process_key(self, key, hold_duration=0):
        now = time.time()
        
        # --- PERBAIKAN LOGIKA TIMEOUT ---
        # Hitung jeda waktu dari tombol terakhir
        elapsed = now - self.last_input_time
        
        # JIKA tombolnya Space, kurangi waktu tahannya.
        # Agar menahan spasi lama tidak dianggap "diam/AFK" oleh sistem.
        if key == "Space":
            elapsed -= hold_duration

        # Cek Timeout (Batas 1.0 detik sesuai soal)
        if elapsed > 1.0 and len(self.current_sequence) > 0:
            print(f"DEBUG: Timeout! Jeda terlalu lama: {elapsed:.2f} detik")
            self.reset_state()
            return "TIMEOUT", None
        # --------------------------------

        self.last_input_time = now
        self.current_sequence.append(key)
        step_index = len(self.current_sequence) - 1

        # Filter Logic
        next_candidates = []
        for combo in self.possible_combos:
            seq = combo['sequence']
            if len(seq) > step_index:
                if key == seq[step_index]:
                    next_candidates.append(combo)
        self.possible_combos = next_candidates

        if not self.possible_combos:
            self.reset_state()
            return "RESET", None

        # Completion Logic
        final_skill = None
        for combo in self.possible_combos:
            if len(combo['sequence']) == len(self.current_sequence):
                final_skill = combo['name']
                
                # Logic Bonus Hold Space
                if key == "Space":
                    print(f"DEBUG: Space ditahan {hold_duration:.2f} detik") # Cek durasi di terminal
                    
                    if 2.0 <= hold_duration <= 3.0:
                        final_skill += " (MAX POWER!!)"
                    elif hold_duration > 3.0:
                        final_skill += " (MISSED TIMING)"
                
                self.reset_state()
                return "SUCCESS", final_skill

        return "CONTINUE", None

class ArcadeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("STREET FIGHTER TRAINER - SPLIT SCREEN")
        self.root.geometry("1000x600") # Layar sedikit dilebarkan
        self.root.configure(bg=BG_COLOR)

        self.combo_file = "combos.json"
        self.engine = None
        self.space_press_time = 0
        self.symbol_map = {"Up": "↑", "Down": "↓", "Left": "←", "Right": "→", "Space": "[SPC]"}
        
        # Simpan referensi tombol menu untuk efek visual
        self.menu_buttons = {} 

        # --- SETUP LAYOUT ---
        # Container Utama (Membagi Kiri dan Kanan)
        main_container = tk.Frame(root, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True)

        # 1. PANEL KIRI (MENU SCROLL)
        self.left_panel = tk.Frame(main_container, bg=SIDEBAR_COLOR, width=300)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False) # Agar lebar tetap fixed 300px

        # 2. PANEL KANAN (GAMEPLAY)
        self.right_panel = tk.Frame(main_container, bg=BG_COLOR)
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Inisialisasi Konten
        self.setup_sidebar()
        self.setup_game_area()

        # Bind Input Keyboard Global
        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)

    # ==============================
    # SETUP UI
    # ==============================
    def setup_sidebar(self):
        # Judul Sidebar
        tk.Label(self.left_panel, text="LIST JURUS", font=("Impact", 20), 
                 bg=SIDEBAR_COLOR, fg="#89b4fa").pack(pady=20)

        # Logic Scrollbar Canvas
        container = tk.Frame(self.left_panel, bg=SIDEBAR_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg=SIDEBAR_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        self.scrollable_frame = tk.Frame(canvas, bg=SIDEBAR_COLOR)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind Mousewheel Scroll
        def _on_mousewheel(event):
            if platform.system() == "Windows":
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            else:
                canvas.yview_scroll(int(-1*event.delta), "units")
        
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Load Tombol
        self.populate_menu_buttons()

    def populate_menu_buttons(self):
        if os.path.exists(self.combo_file):
            with open(self.combo_file, 'r') as f:
                combos = json.load(f)
            
            for c in combos:
                name = c['name']
                # Tombol Menu
                btn = tk.Button(self.scrollable_frame, text=name, font=("Verdana", 11),
                                bg=BOX_COLOR, fg=TEXT_COLOR, anchor="w", padx=20,
                                activebackground=BTN_COLOR, relief="flat", width=25,
                                command=lambda n=name: self.select_combo(n))
                btn.pack(pady=2, fill="x")
                self.menu_buttons[name] = btn
        else:
            tk.Label(self.scrollable_frame, text="File tidak ditemukan!", bg=SIDEBAR_COLOR, fg=ACCENT_COLOR).pack()

    def setup_game_area(self):
        # Placeholder sebelum memilih combo
        self.game_content_frame = tk.Frame(self.right_panel, bg=BG_COLOR)
        self.game_content_frame.pack(fill="both", expand=True, pady=50)

        # 1. Judul Game Area
        self.lbl_title = tk.Label(self.game_content_frame, text="PILIH COMBO DI KIRI", 
                                  font=("Impact", 30), bg=BG_COLOR, fg="#6c7086")
        self.lbl_title.pack(pady=10)

        # 2. Kotak Input Visual
        self.input_box = tk.Frame(self.game_content_frame, bg=BOX_COLOR, height=120)
        self.input_box.pack(fill="x", padx=50, pady=20)
        
        self.lbl_inputs = tk.Label(self.input_box, text="...", 
                                   font=("Consolas", 24, "bold"), bg=BOX_COLOR, fg=TEXT_COLOR)
        self.lbl_inputs.pack(pady=30)

        # 3. Status Text
        self.lbl_status = tk.Label(self.game_content_frame, text="", 
                                   font=("Verdana", 16), bg=BG_COLOR, fg=TEXT_COLOR)
        self.lbl_status.pack(pady=10)

        # 4. Efek Visual Besar
        self.lbl_effect = tk.Label(self.game_content_frame, text="", 
                                   font=("Impact", 40), bg=BG_COLOR, fg=SUCCESS_COLOR)
        self.lbl_effect.pack(pady=20)

        # 5. Instruksi Bawah
        tk.Label(self.right_panel, text="Keyboard: Panah (↑ ↓ ← →) + Spasi [Tahan]", 
                 font=("Arial", 10), bg=BG_COLOR, fg="#585b70").pack(side="bottom", pady=10)

    # ==============================
    # LOGIKA GAMEPLAY
    # ==============================
    def select_combo(self, name):
        # 1. Visual Update Tombol (Highlight yang dipilih)
        for btn_name, btn in self.menu_buttons.items():
            if btn_name == name:
                btn.config(bg=BTN_ACTIVE, fg="#1e1e2e", font=("Verdana", 11, "bold"))
            else:
                btn.config(bg=BOX_COLOR, fg=TEXT_COLOR, font=("Verdana", 11))

        # 2. Reset Engine Game
        self.engine = ComboEngine(self.combo_file, target_combo_name=name)
        
        # 3. Update UI Kanan
        self.lbl_title.config(text=name.upper(), fg=BTN_COLOR)
        self.lbl_inputs.config(text="READY...", fg=TEXT_COLOR)
        self.lbl_status.config(text="Mulai tekan tombol...", fg=TEXT_COLOR)
        self.lbl_effect.config(text="")

        # 4. PENTING: Kembalikan fokus ke window utama agar keyboard langsung jalan
        self.root.focus_set()

    def update_display(self):
        text = " ".join([self.symbol_map.get(k, k) for k in self.engine.current_sequence])
        if not text: text = "READY..."
        self.lbl_inputs.config(text=text)

    def on_key_press(self, event):
        if self.engine is None: return # Belum pilih combo
        
        key = event.keysym
        if key == "space":
            key = "Space"
            if self.space_press_time == 0:
                self.space_press_time = time.time()
                self.lbl_status.config(text="Charging...", fg="#f9e2af")
            return

        if key in ["Up", "Down", "Left", "Right"]:
            self.process_input(key, 0)

    def on_key_release(self, event):
        if self.engine is None: return
        if event.keysym == "space":
            duration = time.time() - self.space_press_time
            self.space_press_time = 0
            self.process_input("Space", duration)

    def process_input(self, key, duration):
        status, skill = self.engine.process_key(key, duration)
        self.update_display()

        if status == "TIMEOUT":
            self.lbl_status.config(text="TIMEOUT!", fg=ACCENT_COLOR)
            self.lbl_effect.config(text="")
            self.flash_bg(ACCENT_COLOR)
            self.update_display()
        elif status == "RESET":
            self.lbl_status.config(text="SALAH INPUT!", fg=ACCENT_COLOR)
            self.update_display()
        elif status == "SUCCESS":
            self.lbl_status.config(text="PERFECT!", fg=SUCCESS_COLOR)
            self.lbl_effect.config(text=f"★ {skill} ★", fg=SUCCESS_COLOR)
            self.flash_bg(SUCCESS_COLOR)
            self.update_display()
        elif status == "CONTINUE":
            self.lbl_status.config(text="Lanjut...", fg="#89b4fa")

    def flash_bg(self, color):
        # Flash hanya area kanan
        orig = self.right_panel.cget("bg")
        self.right_panel.configure(bg=color)
        self.game_content_frame.configure(bg=color)
        self.root.after(100, lambda: [
            self.right_panel.configure(bg=orig),
            self.game_content_frame.configure(bg=orig)
        ])

if __name__ == "__main__":
    if not os.path.exists("combos.json"):
        print("PERINGATAN: File combos.json tidak ditemukan!")
    root = tk.Tk()
    app = ArcadeApp(root)
    root.mainloop()
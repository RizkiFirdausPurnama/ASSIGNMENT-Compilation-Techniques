import tkinter as tk
from tkinter import ttk
import time
import json
import os
import platform
import winsound 

# --- KONFIGURASI WARNA & STYLE ---
BG_COLOR = "#1e1e2e"
SIDEBAR_COLOR = "#181825"
TEXT_COLOR = "#cdd6f4"
ACCENT_COLOR = "#f38ba8"
SUCCESS_COLOR = "#a6e3a1"
SPECIAL_COLOR = "#f9e2af"
BOX_COLOR = "#313244"
BTN_COLOR = "#89b4fa"
BTN_ACTIVE = "#a6e3a1"

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
        elapsed = now - self.last_input_time
        if key == "Space":
            elapsed -= hold_duration 

        if elapsed > 1.0 and len(self.current_sequence) > 0:
            print(f"DEBUG: Timeout! Jeda: {elapsed:.2f}s")
            self.reset_state()
            return "TIMEOUT", None

        self.last_input_time = now
        self.current_sequence.append(key)
        step_index = len(self.current_sequence) - 1

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

        final_skill = None
        for combo in self.possible_combos:
            if len(combo['sequence']) == len(self.current_sequence):
                final_skill = combo['name']
                if key == "Space":
                    print(f"DEBUG: Space ditahan {hold_duration:.2f} detik")
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
        self.root.geometry("1000x600")
        self.root.configure(bg=BG_COLOR)

        # --- UPDATE: MENGGUNAKAN PATH ABSOLUT ---
        # Ini memastikan file selalu dicari di folder script berada
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.combo_file = os.path.join(script_dir, "combos.json")
        # ----------------------------------------
        
        self.engine = None
        self.space_press_time = 0
        self.symbol_map = {"Up": "↑", "Down": "↓", "Left": "←", "Right": "→", "Space": "[SPC]"}
        self.menu_buttons = {} 

        main_container = tk.Frame(root, bg=BG_COLOR)
        main_container.pack(fill="both", expand=True)

        self.left_panel = tk.Frame(main_container, bg=SIDEBAR_COLOR, width=300)
        self.left_panel.pack(side="left", fill="y")
        self.left_panel.pack_propagate(False)

        self.right_panel = tk.Frame(main_container, bg=BG_COLOR)
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.setup_sidebar()
        self.setup_game_area()

        self.root.bind('<KeyPress>', self.on_key_press)
        self.root.bind('<KeyRelease>', self.on_key_release)

    def setup_sidebar(self):
        tk.Label(self.left_panel, text="LIST JURUS", font=("Impact", 20), bg=SIDEBAR_COLOR, fg="#89b4fa").pack(pady=20)
        
        container = tk.Frame(self.left_panel, bg=SIDEBAR_COLOR)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(container, bg=SIDEBAR_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=SIDEBAR_COLOR)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def _on_mousewheel(event):
            delta = int(-1*(event.delta/120)) if platform.system() == "Windows" else int(-1*event.delta)
            canvas.yview_scroll(delta, "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        self.populate_menu_buttons()

    def populate_menu_buttons(self):
        if os.path.exists(self.combo_file):
            with open(self.combo_file, 'r') as f:
                combos = json.load(f)
            for c in combos:
                name = c['name']
                btn = tk.Button(self.scrollable_frame, text=name, font=("Verdana", 11),
                                bg=BOX_COLOR, fg=TEXT_COLOR, anchor="w", padx=20,
                                activebackground=BTN_COLOR, relief="flat", width=25,
                                command=lambda n=name: self.select_combo(n))
                btn.pack(pady=2, fill="x")
                self.menu_buttons[name] = btn
        else:
            tk.Label(self.scrollable_frame, text="File tidak ditemukan!", bg=SIDEBAR_COLOR, fg=ACCENT_COLOR).pack()

    def setup_game_area(self):
        self.game_content_frame = tk.Frame(self.right_panel, bg=BG_COLOR)
        self.game_content_frame.pack(fill="both", expand=True, pady=50)

        self.lbl_title = tk.Label(self.game_content_frame, text="PILIH COMBO DI KIRI", font=("Impact", 30), bg=BG_COLOR, fg="#6c7086")
        self.lbl_title.pack(pady=10)

        self.input_box = tk.Frame(self.game_content_frame, bg=BOX_COLOR, height=120)
        self.input_box.pack(fill="x", padx=50, pady=20)
        self.lbl_inputs = tk.Label(self.input_box, text="...", font=("Consolas", 24, "bold"), bg=BOX_COLOR, fg=TEXT_COLOR)
        self.lbl_inputs.pack(pady=30)

        self.lbl_status = tk.Label(self.game_content_frame, text="", font=("Verdana", 16), bg=BG_COLOR, fg=TEXT_COLOR)
        self.lbl_status.pack(pady=10)

        self.lbl_effect = tk.Label(self.game_content_frame, text="", font=("Impact", 40), bg=BG_COLOR, fg=SUCCESS_COLOR)
        self.lbl_effect.pack(pady=20)

        tk.Label(self.right_panel, text="Keyboard: Panah (↑ ↓ ← →) + Spasi [Tahan 2-3s]", font=("Arial", 10), bg=BG_COLOR, fg="#585b70").pack(side="bottom", pady=10)

    def select_combo(self, name):
        for btn_name, btn in self.menu_buttons.items():
            if btn_name == name:
                btn.config(bg=BTN_ACTIVE, fg="#1e1e2e", font=("Verdana", 11, "bold"))
            else:
                btn.config(bg=BOX_COLOR, fg=TEXT_COLOR, font=("Verdana", 11))

        self.engine = ComboEngine(self.combo_file, target_combo_name=name)
        self.lbl_title.config(text=name.upper(), fg=BTN_COLOR)
        self.lbl_inputs.config(text="READY...", fg=TEXT_COLOR)
        self.lbl_status.config(text="Mulai tekan tombol...", fg=TEXT_COLOR)
        self.lbl_effect.config(text="")
        self.root.focus_set()

    def update_display(self):
        text = " ".join([self.symbol_map.get(k, k) for k in self.engine.current_sequence])
        if not text: text = "READY..."
        self.lbl_inputs.config(text=text)

    def on_key_press(self, event):
        if self.engine is None: return
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

    def trigger_sound(self, is_special):
        try:
            # Gunakan path absolut untuk mencari file suara juga
            script_dir = os.path.dirname(os.path.abspath(__file__))
            
            if is_special:
                wav_path = os.path.join(script_dir, "special.wav")
                if os.path.exists(wav_path):
                    winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.Beep(1500, 500) 
            else:
                wav_path = os.path.join(script_dir, "hit.wav")
                if os.path.exists(wav_path):
                    winsound.PlaySound(wav_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                else:
                    winsound.Beep(800, 150)
        except Exception:
            pass

    def process_input(self, key, duration):
        status, skill = self.engine.process_key(key, duration)
        self.update_display()

        if status == "TIMEOUT":
            self.lbl_status.config(text="TIMEOUT!", fg=ACCENT_COLOR)
            self.lbl_effect.config(text="")
            self.flash_bg(ACCENT_COLOR)
            
        elif status == "RESET":
            self.lbl_status.config(text="SALAH INPUT!", fg=ACCENT_COLOR)
            
        elif status == "SUCCESS":
            is_max_power = "(MAX POWER!!)" in skill
            if is_max_power:
                self.lbl_status.config(text="PERFECT EXECUTION!", fg=SPECIAL_COLOR)
                self.lbl_effect.config(text=f"★ {skill} ★", fg=SPECIAL_COLOR)
                self.flash_bg(SPECIAL_COLOR) 
                self.trigger_sound(is_special=True)
            else:
                self.lbl_status.config(text="NICE!", fg=SUCCESS_COLOR)
                self.lbl_effect.config(text=f"{skill}", fg=SUCCESS_COLOR)
                self.flash_bg(SUCCESS_COLOR)
                self.trigger_sound(is_special=False)
                
        elif status == "CONTINUE":
            self.lbl_status.config(text="Lanjut...", fg="#89b4fa")

    def flash_bg(self, color):
        orig = self.right_panel.cget("bg")
        self.right_panel.configure(bg=color)
        self.game_content_frame.configure(bg=color)
        self.root.after(100, lambda: [
            self.right_panel.configure(bg=orig),
            self.game_content_frame.configure(bg=orig)
        ])

if __name__ == "__main__":
    # --- UPDATE: CHECK FILE DI FOLDER SCRIPT ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(script_dir, "combos.json")

    if not os.path.exists(json_path):
        print(f"PERINGATAN: File combos.json tidak ditemukan di: {json_path}")
        print("Pastikan file 'combos.json' ada di folder yang sama dengan 'Game.py'")
    # -------------------------------------------

    root = tk.Tk()
    app = ArcadeApp(root)
    root.mainloop()
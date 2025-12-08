import time

class Combo:
    def __init__(self, name, sequence):
        self.name = name
        self.sequence = sequence


COMBO_LIST = [
    Combo("Hadoken", ["→", "→", "→", "Space"]),
    Combo("Shoryuken", ["↑", "↓", "↑", "→", "Space"]),
    Combo("Tatsumaki", ["←", "→", "←", "→", "Space"]),
    Combo("Dragon Punch", ["↑", "↑", "↓", "→", "Space"]),
    Combo("Hurricane Kick", ["→", "↓", "→", "→", "Space"]),
    Combo("Giga Hadoken", ["→", "→", "→", "↓", "↑", "→", "Space"]),
    Combo("Ultra Shoryuken", ["→", "→", "↓", "→", "↑", "↓", "→", "Space"]),
    Combo("Mega Tatsumaki", ["↑", "↑", "↓", "→", "→", "→", "→", "Space"]),
    Combo("Final Dragon Punch", ["←", "↑", "→", "→", "↓", "↑", "→", "Space"]),
    Combo("Ultimate Hurricane Kick", ["→", "→", "↑", "↓", "→", "↑", "→", "→", "Space"])
]


class StateMachine:
    """
    Engine utama yang menangani logika deteksi combo (FSM).
    """
    def __init__(self):
        self.reset_state()

    def reset_state(self):
        """Kembali ke State Awal (S0) dan reset semua tracking."""
        self.current_input_sequence = []
        self.last_input_time = time.time()
        self.possible_combos = COMBO_LIST[:] 
        print(f"\n[SYSTEM] State Reset. Ready for Input.")

    def process_input(self, key, hold_duration=0):
        """
        Memproses satu tombol yang ditekan.
        Return: String nama skill jika berhasil, None jika belum.
        """
        now = time.time()
        
        # 1. Cek Timeout (Syarat: Reset jika > 1 detik)
        if now - self.last_input_time > 1.0 and len(self.current_input_sequence) > 0:
            print("[TIMEOUT] Combo gagal karena jeda > 1 detik.")
            self.reset_state()

        self.last_input_time = now
        
        self.current_input_sequence.append(key)
        current_step_index = len(self.current_input_sequence) - 1
        
        print(f"   -> Input masuk: {key} (Step ke-{current_step_index + 1})")

        # 2. Filter Kandidat (Logika Anti-Overlap)
        next_candidates = []
        
        for combo in self.possible_combos:
            if len(combo.sequence) > current_step_index:
                expected_key = combo.sequence[current_step_index]
                if key == expected_key:
                    next_candidates.append(combo)

        self.possible_combos = next_candidates

        # 3. Cek apakah ada combo yang GAGAL total (Kandidat kosong)
        if not self.possible_combos:
            print("[FAIL] Tidak ada combo yang cocok. Resetting...")
            self.reset_state()
            return None

        # 4. Cek apakah ada combo yang SELESAI (Completed)
        completed_combo = None
        
        for combo in self.possible_combos:
            if len(combo.sequence) == len(self.current_input_sequence):
                completed_combo = combo
                break

        if completed_combo:
            # 5. Cek Syarat Space Hold (Bonus 10 Poin)
            final_skill_name = completed_combo.name
            
            if key == "Space":
                if 2.0 <= hold_duration <= 3.0:
                    final_skill_name += " (MAX POWER!! - Hold Bonus)"
                    print(f"[EFFECT] Aura meledak! Space ditahan {hold_duration:.2f} detik.")
                elif hold_duration > 3.0:
                    final_skill_name += " (Missed Timing - Too Long)"
                else:
                    final_skill_name += " (Normal Hit)"

            print(f"*** COMBO EXECUTED: {final_skill_name} ***")
            self.reset_state()
            return final_skill_name

        return None


class GameSystem:
    def __init__(self):
        self.engine = StateMachine()

    def start(self):
        print("=== STREET FIGHTER COMBO SYSTEM (OOP) ===")
        print("Daftar Tombol: →, ↓, ↑, ←, Space")
        print("Ketik 'exit' untuk keluar.\n")
        print("Cara pakai:")
        print("1. Ketik simbol panah untuk input biasa.")
        print("2. Ketik 'Space' saja untuk spasi cepat.")
        print("3. Ketik 'Space 2.5' untuk simulasi tahan spasi 2.5 detik.")
        
        while True:
            raw_input = input("\nMasukkan Tombol: ").strip()
            
            if raw_input.lower() == "exit":
                break
            
            key = raw_input
            duration = 0.0
        
            if raw_input.startswith("Space") and " " in raw_input:
                parts = raw_input.split()
                key = parts[0]
                try:
                    duration = float(parts[1])
                except ValueError:
                    duration = 0.0
            
            valid_keys = ["→", "↓", "↑", "←", "Space"]
            if key not in valid_keys:
                print("Tombol tidak valid. Gunakan: →, ↓, ↑, ←, Space")
                continue

            self.engine.process_input(key, duration)

if __name__ == "__main__":
    game = GameSystem()
    game.start()
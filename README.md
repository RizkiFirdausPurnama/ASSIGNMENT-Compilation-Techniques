# Compilation Techniques: Automata Project

**Automata Project** adalah tugas kelompok mata kuliah *Compilation Techniques* yang mengimplementasikan teori Automata (Pushdown Automata & Finite State Machine) ke dalam aplikasi perangkat lunak berbasis **Object-Oriented Programming (OOP)**.

Project ini terdiri dari dua modul terpisah: **Math Converter** (Web App) dan **Fighting Game Engine** (Desktop App).



---

## 🛠️ Teknologi yang Digunakan

**Bahasa Pemrograman:**
* **Python 3.10+** - Core Logic

**Modul 1 (Math Converter):**
* **Streamlit** - Framework Web UI
* **Regex (Re)** - Lexical Analysis & Tokenizing
* **Collections (List)** - Stack Implementation

**Modul 2 (Game Engine):**
* **Tkinter** - GUI Library (Desktop)
* **Winsound** - Audio Feedback (Windows System)
* **JSON** - Data Storage untuk Combo List
* **Time** - Manajemen State Timer

---

## ✨ Fitur Utama

### 🧮 Modul 1: Math Notation Converter (PDA)
Implementasi **Pushdown Automata** untuk memvalidasi dan mengonversi rumus matematika.

1.  **Lexical Analyzer (Tokenizer):**
    * Mampu membaca input rumus tanpa spasi (contoh: `(3+5)*2`) menggunakan Regex.
    * Memisahkan operand (angka) dan operator secara cerdas.
2.  **Validasi Rumus:**
    * Mengecek keseimbangan kurung `( )`.
    * Memastikan urutan operand dan operator sesuai kaidah matematika (Infix/Prefix/Postfix).
3.  **Konversi Multi-Format:**
    * **Infix ↔ Postfix ↔ Prefix:** Konversi akurat antar ketiga format notasi.
4.  **Visualisasi Stack:**
    * Menampilkan detail proses tokenizing di layar untuk kebutuhan presentasi.

### 🎮 Modul 2: Fighting Game Input Engine (FSM)
Implementasi **Finite State Machine** untuk mendeteksi jurus game fighting dengan batasan waktu.

1.  **Combo Detection System:**
    * Mendeteksi 10 jenis jurus berdasarkan urutan tombol yang ditekan.
    * Menggunakan file `combos.json` eksternal sehingga daftar jurus mudah diedit.
2.  **Strict Timer Mechanism:**
    * **1-Second Rule:** State akan reset otomatis jika jeda antar tombol lebih dari 1 detik.
3.  **Charged Attack (Bonus):**
    * Mendeteksi jika tombol `Space` terakhir ditahan selama **2-3 detik**.
    * Memberikan output "MAX POWER" dan efek suara khusus jika timing tepat.
4.  **Interactive Feedback:**
    * Visual: Layar berkedip hijau (Sukses) atau merah (Timeout).
    * Audio: Efek suara *hit* dan *special move*.

---

## 🚀 Cara Menjalankan Proyek

Proyek ini memiliki dua aplikasi berbeda. Pastikan Anda sudah menginstall Python sebelum memulai.

### Prasyarat
Install library Streamlit untuk Modul 1:
```bash
pip install streamlit
```

### 1. Menjalankan Modul 1 (Math Converter)

1.  Buka terminal/CMD, arahkan ke folder proyek.
2.  Jalankan perintah berikut:
    ```bash
    streamlit run "Pushdown Automata(PDA)no.1.py"
    ```
    *(Pastikan nama file python sesuai dengan file Anda)*
> 🖥️ **Aplikasi akan terbuka otomatis di browser default Anda.**

### 2. Menjalankan Modul 2 (Game Engine)

**PENTING:** Sebelum menjalankan, Anda **WAJIB** membuat file database jurus terlebih dahulu.

1.  Buat file baru bernama `combos.json` di folder yang sama dengan script game.
2.  Salin kode JSON berikut ke dalamnya:
    ```json
    [
      { "name": "Hadoken", "sequence": ["Right", "Right", "Right", "Space"] },
      { "name": "Shoryuken", "sequence": ["Up", "Down", "Up", "Right", "Space"] },
      { "name": "Tatsumaki", "sequence": ["Left", "Right", "Left", "Right", "Space"] },
      { "name": "Dragon Punch", "sequence": ["Up", "Up", "Down", "Right", "Space"] },
      { "name": "Hurricane Kick", "sequence": ["Right", "Down", "Right", "Right", "Space"] },
      { "name": "Giga Hadoken", "sequence": ["Right", "Right", "Right", "Down", "Up", "Right", "Space"] },
      { "name": "Ultra Shoryuken", "sequence": ["Right", "Right", "Down", "Right", "Up", "Down", "Right", "Space"] },
      { "name": "Mega Tatsumaki", "sequence": ["Up", "Up", "Down", "Right", "Right", "Right", "Right", "Space"] },
      { "name": "Final Dragon Punch", "sequence": ["Left", "Up", "Right", "Right", "Down", "Up", "Right", "Space"] },
      { "name": "Ultimate Hurricane Kick", "sequence": ["Right", "Right", "Up", "Down", "Right", "Up", "Right", "Right", "Space"] }
    ]
    ```
3.  Jalankan game dengan perintah:
    ```bash
    python soal2_game.py
    ```
> 🕹️ **Jendela GUI akan muncul. Gunakan tombol panah keyboard dan Spasi untuk bermain.**

---

## 🏗️ Arsitektur Software (OOP)

Kode program disusun menggunakan paradigma *Object-Oriented Programming* untuk modularitas dan kemudahan maintenance.

**Class Diagram Overview:**

* **MathAutomata (Logic):** Menangani stack operation dan validasi logika PDA.
* **ComboEngine (Logic):** Menangani perpindahan state FSM, timer, dan validasi input array.
* **ArcadeApp (UI):** Menangani tampilan Tkinter, event binding, dan visual feedback.

---

## 👥 Tim Penyusun

* **Anggota 1:** [Rizki Firdaus Punama] 
* **Anggota 2:** [Stanley Christian Dermawan] 
* **Anggota 3:** [Marecellus Geraldio Florenta]
* **Anggota 4:** [Rio Fredinan] 
* **Anggota 5:** [Rafi Satria] 

**Institusi:** Binus University - School of Computer Science
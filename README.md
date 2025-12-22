# Compilation Techniques: Automata Project

**Course:** Compilation Techniques  
**Submission Date:** December 8th  


---

## 📋 Project Overview

This repository contains the solution for the Compilation Techniques Group Assignment. The project is divided into two main modules based on Object-Oriented Programming (OOP) principles:

1.  **Math Notation Converter (Pushdown Automata)**
2.  **Fighting Game Combo Detector (Finite State Machine)**

---

## 🛠️ Module 1: Math Notation Converter
**Type:** Pushdown Automata (PDA)

This module validates mathematical formulas and converts them between Infix, Postfix, and Prefix notations using a Stack-based approach (PDA).

### Features
* [cite_start]**Validation:** Checks if the input formula is valid based on Infix, Postfix, or Prefix rules[cite: 10].
* [cite_start]**Supported Symbols:** Accepts digits (0-9) and basic operators (`+`, `-`, `*`, `/`)[cite: 11].
* [cite_start]**Conversion:** Converts any valid input format to the other two formats (e.g., Infix to Prefix, Prefix to Postfix)[cite: 12, 13].

### Automata Diagram
> *[Place your Pushdown Automata (PDA) Diagram image here]* > *Description: The state transition diagram showing how the stack handles operators and operands.*

---

## 🎮 Module 2: Fighting Game Input Engine
**Type:** Finite State Machine (FSM)

This module simulates a fighting game input system that detects specific key combinations (combos) within a time limit.

### Features
* [cite_start]**Combo Detection:** Identifies 10 specific move sequences based on the assignment table[cite: 16].
* **Time Constraint:** Implements a strict **1-second timer** between inputs. [cite_start]If the gap exceeds 1 second, the state machine resets to the initial state[cite: 19, 20].
* [cite_start]**Charged Attack (Bonus):** Detects if the final `Space` key is held for **2-3 seconds** to trigger a special effect/output[cite: 21].

### Combo List
The system detects the following sequences:

| No | Input Sequence | Combo Output |
| :--- | :--- | :--- |
| 1 | `→` `→` `→` Space | Hadoken |
| 2 | `↑` `↓` `↑` `→` Space | Shoryuken |
| 3 | `←` `→` `←` `→` Space | Tatsumaki |
| 4 | `↑` `↑` `↓` `→` Space | Dragon Punch |
| 5 | `→` `↓` `→` `→` Space | Hurricane Kick |
| 6 | `→` `→` `→` `↓` `↑` `→` Space | Giga Hadoken |
| 7 | `→` `→` `↓` `→` `↑` `↓` `→` Space | Ultra Shoryuken |
| 8 | `↑` `↑` `↓` `→` `→` `→` `→` Space | Mega Tatsumaki |
| 9 | `←` `↑` `→` `→` `↓` `↑` `→` Space | Final Dragon Punch |
| 10 | `→` `→` `↑` `↓` `→` `↑` `→` `→` Space | Ultimate Hurricane Kick |

[cite_start]*[cite: 18]*

### Automata Diagram
> *[Place your State Machine Diagram image here]* > *Description: The FSM diagram showing state transitions for each key press and the timeout reset loop.*

---

## ⚙️ Installation & Usage

### Prerequisites
* [Programming Language, e.g., Python 3.10+ / Java 17 / C#]
* [Any specific libraries if used]

### How to Run
1.  Clone the repository:
    ```bash
    git clone [https://github.com/your-repo/automata-assignment.git](https://github.com/your-repo/automata-assignment.git)
    ```
2.  Navigate to the directory:
    ```bash
    cd automata-assignment
    ```
3.  Run the main program:
    ```bash
    # Example command
    python main.py
    ```

---

## 🏗️ Software Architecture
[cite_start]The solution utilizes **Object-Oriented Programming (OOP)**  to ensure modularity and code quality:
* **Classes:** Separate classes for `StackHandler`, `Converter`, `ComboDetector`, and `Timer`.
* **State Pattern:** Used for the Fighting Game module to manage input states cleanly.

---

## 📸 Screenshots
> *[Add screenshots of the program running (Console or GUI) here]*
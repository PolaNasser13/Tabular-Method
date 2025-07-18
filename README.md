# Tabular Method GUI Tool (SOP / POS Simplifier)

A graphical desktop tool to simplify Boolean expressions using the **Tabular Method** (also known as the **Quine–McCluskey algorithm**) for both:
- **Sum of Products (SOP)**
- **Product of Sums (POS)**

---

## 🖥️ Features

- Built using `Tkinter` for GUI interaction.
- Supports both **minterms** and **maxterms** input.
- Displays:
  - Prime Implicants
  - Essential Prime Implicants
  - Final simplified Boolean expression (SOP or POS).
- Optional support for **Don't Care** conditions.
- Friendly interface with step-by-step flow.

---

## 📷 GUI Screenshots

<img width="1277" height="918" alt="image" src="https://github.com/user-attachments/assets/4387d2d1-18f5-4218-8e14-318aeadc5ea7" />

---

## 🚀 How to Run

### 1. Requirements

- Python 3.x  
(Tkinter is included with Python by default.)

### 2. Run the script:

```bash
python "Tabular method.py"
```

## 🧠 How It Works

The tool takes in:  
- Number of variables  
- Minterms or Maxterms  
- (Optional) Don't Care terms  

Then it:  
- Converts inputs into binary form.  
- Groups terms by the number of 1s.  
- Iteratively combines terms using the tabular method.  
- Identifies Prime Implicants and Essential Prime Implicants.  
- Constructs the minimized Boolean expression in either SOP or POS form.

## 👤 Author

- Name: Pola Nasser Ayoub  
- Faculty: Faculty of Engineering, Alexandria University  
- Department: Computers and Communications Engineering (CCE)

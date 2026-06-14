import tkinter as tk
from tkinter import filedialog, messagebox
import json
import copy

grammar = {}

root = tk.Tk()
root.title("GNF Dönüştürücü")
root.geometry("1000x700")
root.configure(bg="#2b2b2b")

title_label = tk.Label(
    root,
    text="Gramerden Greibach Normal Formuna Dönüştürücü",
    bg="#2b2b2b",
    fg="white",
    font=("Arial", 16, "bold")
)
title_label.pack(pady=10)

text_area = tk.Text(
    root,
    font=("Consolas", 10),
    bg="#1e1e1e",
    fg="#00ff99",
    insertbackground="white",
    wrap="word"
)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")

text_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_area.yview)

text_area.pack(fill="both", expand=True, padx=10, pady=10)


def show_grammar(title, g):
    text_area.insert(tk.END, f"\n=== {title} ===\n\n")

    for left, rights in g["productions"].items():
        rules = []

        for r in rights:
            rules.append("".join(r))

        line = left + " -> " + " | ".join(rules)
        text_area.insert(tk.END, line + "\n")

    text_area.insert(tk.END, "\n")


def load_grammar():

    global grammar

    file_path = filedialog.askopenfilename(
        title="Dosya Seç",
        filetypes=[
            ("Tüm desteklenen dosyalar", "*.json *.txt *.xlsx"),
            ("JSON dosyaları", "*.json"),
            ("TXT dosyaları", "*.txt"),
            ("Excel dosyaları", "*.xlsx"),
            ("Tüm dosyalar", "*.*")
        ]
    )

    if not file_path:
        return

    try:
        file_path_lower = file_path.lower()

        if file_path_lower.endswith(".json"):
            with open(file_path, "r", encoding="utf-8") as file:
                grammar = json.load(file)

        elif file_path_lower.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

            grammar = parse_txt(lines)

        elif file_path_lower.endswith(".xlsx"):
            df = pd.read_excel(file_path)

            lines = []

            for _, row in df.iterrows():
                left = str(row.iloc[0]).strip()
                right = str(row.iloc[1]).strip()

                lines.append(f"{left} -> {right}")

            grammar = parse_txt(lines)

        else:
            messagebox.showerror("Hata", "Desteklenmeyen dosya türü.")
            return

        text_area.delete(1.0, tk.END)

        text_area.insert(tk.END, "CFG başarıyla dosyadan yüklendi.\n")
        text_area.insert(tk.END, f"\nDosya: {file_path}\n")
        text_area.insert(tk.END, f"Dosya Türü: {file_path_lower.split('.')[-1].upper()}\n")

        show_grammar("ORİJİNAL CFG", grammar)

    except Exception as e:
        messagebox.showerror(
            "Hata",
            f"Dosya okunamadı:\n{e}"
        )

def remove_epsilon():
    global grammar

    if not grammar:
        messagebox.showwarning("Uyarı", "Önce JSON dosyası yükleyin.")
        return

    new_grammar = copy.deepcopy(grammar)
    nullable = []

    for left, rights in grammar["productions"].items():
        for r in rights:
            if r == ["ε"]:
                nullable.append(left)

    for left, rights in grammar["productions"].items():
        new_rules = []

        for r in rights:
            if r not in new_rules:
                new_rules.append(r)

            for n in nullable:
                if n in r:
                    temp = [x for x in r if x != n]

                    if temp and temp not in new_rules:
                        new_rules.append(temp)

        cleaned = []

        for rule in new_rules:
            if rule != ["ε"] and rule not in cleaned:
                cleaned.append(rule)

        new_grammar["productions"][left] = cleaned

    grammar = new_grammar

    show_grammar("EPSILON TEMİZLENMİŞ CFG", grammar)


def remove_unit():
    global grammar

    if not grammar:
        messagebox.showwarning("Uyarı", "Önce JSON dosyası yükleyin.")
        return

    new_grammar = copy.deepcopy(grammar)

    for left, rights in grammar["productions"].items():
        updated = []

        for r in rights:
            if len(r) == 1 and r[0] in grammar["variables"]:
                target = r[0]

                for target_rule in grammar["productions"].get(target, []):
                    if target_rule not in updated:
                        updated.append(target_rule)
            else:
                if r not in updated:
                    updated.append(r)

        new_grammar["productions"][left] = updated

    grammar = new_grammar

    show_grammar("BİRİM ÜRETİMLER TEMİZLENDİ", grammar)


def parse_txt(lines):

    variables = set()
    terminals = set()
    productions = {}

    start_symbol = None

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "->" not in line:
            continue

        left, right = line.split("->")

        left = left.strip()

        if start_symbol is None:
            start_symbol = left

        variables.add(left)

        rules = right.split("|")

        prod_list = []

        for r in rules:

            r = r.strip()

            symbols = []

            for ch in r:

                if ch == " ":
                    continue

                symbols.append(ch)

                if ch.isupper():
                    variables.add(ch)

                elif ch != "ε":
                    terminals.add(ch)

            prod_list.append(symbols)

        productions[left] = prod_list

    return {
        "variables": list(variables),
        "terminals": list(terminals),
        "start": start_symbol,
        "productions": productions
    }

def convert_gnf():
    global grammar

    if not grammar:
        messagebox.showwarning("Uyarı", "Önce JSON dosyası yükleyin.")
        return

    new_grammar = copy.deepcopy(grammar)

    max_steps = 20
    step = 0

    while step < max_steps:
        step += 1
        changed = False

        for left, rights in list(new_grammar["productions"].items()):
            updated_rules = []

            for rule in rights:
                if not rule:
                    continue

                first = rule[0]

                if first in new_grammar["terminals"]:
                    if rule not in updated_rules:
                        updated_rules.append(rule)

                elif first in new_grammar["variables"]:
                    remaining_part = rule[1:]

                    if first == left:
                        if rule not in updated_rules:
                            updated_rules.append(rule)
                        continue

                    for replacement in new_grammar["productions"].get(first, []):
                        if not replacement:
                            continue

                        if replacement[0] == first:
                            continue

                        new_rule = replacement + remaining_part

                        if new_rule not in updated_rules:
                            updated_rules.append(new_rule)
                            changed = True

                else:
                    if rule not in updated_rules:
                        updated_rules.append(rule)

            new_grammar["productions"][left] = updated_rules

        if not changed:
            break

    grammar = new_grammar

    show_grammar("GNF'YE DÖNÜŞTÜRÜLMÜŞ GRAMER", grammar)

    text_area.insert(tk.END, "=== GNF KONTROLÜ ===\n")

    for left, rights in grammar["productions"].items():
        for r in rights:
            first = r[0]

            if first in grammar["terminals"]:
                text_area.insert(
                    tk.END,
                    f"{left} -> {''.join(r)}  ✓ GNF uygun\n"
                )
            else:
                text_area.insert(
                    tk.END,
                    f"{left} -> {''.join(r)}  ✗ GNF uygun değil\n"
                )

    if step >= max_steps:
        text_area.insert(
            tk.END,
            "\nUYARI: Bazı kurallarda döngü olduğu için dönüşüm sınırlandırıldı.\n"
        )

    text_area.insert(tk.END, "\n")


def clear_screen():
    text_area.delete(1.0, tk.END)


button_frame = tk.Frame(root, bg="#2b2b2b")
button_frame.pack(pady=10)

button_style = {
    "width": 14,
    "bg": "#404040",
    "fg": "white",
    "font": ("Arial", 11, "bold"),
    "activebackground": "#606060",
    "activeforeground": "white"
}

load_button = tk.Button(
    button_frame,
    text="Dosya Yükle",
    command=load_grammar,
    **button_style
)
load_button.grid(row=0, column=0, padx=5)

epsilon_button = tk.Button(
    button_frame,
    text="ε Temizle",
    command=remove_epsilon,
    **button_style
)
epsilon_button.grid(row=0, column=1, padx=5)

unit_button = tk.Button(
    button_frame,
    text="Birim Üretim Temizle",
    command=remove_unit,
    **button_style
)
unit_button.grid(row=0, column=2, padx=5)

gnf_button = tk.Button(
    button_frame,
    text="GNF'ye Dönüştür",
    command=convert_gnf,
    **button_style
)
gnf_button.grid(row=0, column=3, padx=5)

clear_button = tk.Button(
    button_frame,
    text="Ekranı Temizle",
    command=clear_screen,
    **button_style
)
clear_button.grid(row=0, column=4, padx=5)

root.mainloop()